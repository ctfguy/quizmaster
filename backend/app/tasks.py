from celery import Celery
from flask import current_app
from app.extensions import db
from app.models import User, Quiz, Score
from datetime import datetime, timedelta
import csv
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pdfkit 

celery = Celery(__name__)

@celery.task
def send_daily_reminders():
    with current_app.app_context():
        users = User.query.filter_by(role='user').all()
        
        recent_quizzes = Quiz.query.filter(
            Quiz.date_of_quiz >= datetime.utcnow() - timedelta(days=1)
        ).all()
        
        if recent_quizzes:
            for user in users:
                user_scores = Score.query.filter_by(user_id=user.id).all()
                attempted_quiz_ids = [score.quiz_id for score in user_scores]
                
                new_quizzes = [quiz for quiz in recent_quizzes if quiz.id not in attempted_quiz_ids]
                
                if new_quizzes:
                    quiz_list = "\n".join([f"- {quiz.chapter.name}: {quiz.date_of_quiz.strftime('%Y-%m-%d %H:%M')}" 
                                          for quiz in new_quizzes])
                    
                    send_email(
                        user.email,
                        "New Quizzes Available",
                        f"Hello {user.full_name},\n\nThere are {len(new_quizzes)} new quizzes available:\n\n{quiz_list}\n\nRegards,\nQuiz Master Team"
                    )

@celery.task
def generate_monthly_report():
    with current_app.app_context():
        users = User.query.filter_by(role='user').all()
        
        now = datetime.utcnow()
        month_start = datetime(now.year, now.month, 1)
        prev_month = now.month - 1 if now.month > 1 else 12
        prev_year = now.year if now.month > 1 else now.year - 1
        prev_month_start = datetime(prev_year, prev_month, 1)
        
        for user in users:
            scores = Score.query.filter(
                Score.user_id == user.id,
                Score.time_stamp_of_attempt >= prev_month_start,
                Score.time_stamp_of_attempt < month_start
            ).all()
            
            if scores:
                total_quizzes = len(scores)
                avg_score = sum(score.total_scored for score in scores) / total_quizzes if total_quizzes > 0 else 0
                
                html_report = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; }}
                        h1 {{ color: #4a86e8; }}
                        table {{ border-collapse: collapse; width: 100%; }}
                        th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                        th {{ background-color: #f2f2f2; }}
                    </style>
                </head>
                <body>
                    <h1>Monthly Activity Report</h1>
                    <p>Hello {user.full_name},</p>
                    <p>Here is your activity report for {prev_month}/{prev_year}:</p>
                    
                    <h2>Summary</h2>
                    <p>Total quizzes taken: {total_quizzes}</p>
                    <p>Average score: {avg_score:.2f}%</p>
                    
                    <h2>Details</h2>
                    <table>
                        <tr>
                            <th>Quiz</th>
                            <th>Date</th>
                            <th>Score</th>
                            <th>Percentage</th>
                        </tr>
                """
                
                for score in scores:
                    quiz = Quiz.query.get(score.quiz_id)
                    chapter = quiz.chapter if quiz else None
                    quiz_name = f"{chapter.name}" if chapter else f"Quiz {score.quiz_id}"
                    
                    percentage = (score.total_scored / score.total_possible * 100) if score.total_possible > 0 else 0
                    html_report += f"""
                        <tr>
                            <td>{quiz_name}</td>
                            <td>{score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M')}</td>
                            <td>{score.total_scored}/{score.total_possible}</td>
                            <td>{percentage:.2f}%</td>
                        </tr>
                    """
                
                html_report += """
                    </table>
                    <p>Keep up the good work!</p>
                    <p>Regards,<br>Quiz Master Team</p>
                </body>
                </html>
                """
                
                # Generate PDF from HTML
                pdf_file = pdfkit.from_string(html_report, False)
                
                # Send email with PDF attachment
                send_email_with_attachment(
                    user.email,
                    f"Monthly Activity Report - {prev_month}/{prev_year}",
                    "Please find your monthly activity report attached.",
                    pdf_file,
                    f"activity_report_{prev_month}_{prev_year}.pdf"
                )

@celery.task
def export_quiz_data(user_id=None):
    with current_app.app_context():
        output = io.StringIO()
        writer = csv.writer(output)
        
        if user_id:
            scores = Score.query.filter_by(user_id=user_id).all()
            writer.writerow(['Quiz ID', 'Date Attempted', 'Score', 'Total Possible', 'Percentage'])
            
            for score in scores:
                percentage = (score.total_scored / score.total_possible * 100) if score.total_possible > 0 else 0
                writer.writerow([
                    score.quiz_id,
                    score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M'),
                    score.total_scored,
                    score.total_possible,
                    f"{percentage:.2f}%"
                ])
        else:
            users = User.query.filter_by(role='user').all()
            writer.writerow(['User ID', 'Email', 'Full Name', 'Quizzes Taken', 'Average Score'])
            
            for user in users:
                scores = Score.query.filter_by(user_id=user.id).all()
                quizzes_taken = len(scores)
                avg_score = sum(score.total_scored for score in scores) / quizzes_taken if quizzes_taken > 0 else 0
                writer.writerow([
                    user.id,
                    user.email,
                    user.full_name,
                    quizzes_taken,
                    f"{avg_score:.2f}%"
                ])
        
        csv_data = output.getvalue()
        output.close()
        
        return csv_data

def send_email(to, subject, body, html_content=None):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
    msg['To'] = to
    
    part1 = MIMEText(body, 'plain')
    msg.attach(part1)
    
    if html_content:
        part2 = MIMEText(html_content, 'html')
        msg.attach(part2)
    
    try:
        server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        server.starttls()
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_email_with_attachment(to, subject, body, attachment_data, attachment_name):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
    msg['To'] = to
    
    msg.attach(MIMEText(body))
    
    attachment = MIMEText(attachment_data, 'base64')
    attachment.add_header('Content-Disposition', 'attachment', filename=attachment_name)
    msg.attach(attachment)
    
    try:
        server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        server.starttls()
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False