from app import create_app
from app.tasks import celery
import datetime
import time

# Create the Flask app context
app = create_app()
app_context = app.app_context()
app_context.push()

def test_simple_task():
    """Test a simple task that just returns success after delay"""
    print("Submitting test task...")
    
    # Create a simple task that just returns a message
    @celery.task(name="test.simple_task")
    def simple_task():
        time.sleep(2)  # Simulate work
        return {"status": "success", "timestamp": datetime.datetime.now().isoformat()}
    
    # Submit the task
    result = simple_task.delay()
    print(f"Task submitted with ID: {result.id}")
    
    # Wait for task completion
    print("Waiting for task to complete...")
    task_result = result.get(timeout=10)
    
    print(f"Task completed with result: {task_result}")
    return task_result

def test_email_task():
    """Test email reminder task functionality"""
    from app.tasks import send_quiz_reminder_emails
    
    print("Submitting email reminder task...")
    task = send_quiz_reminder_emails.delay()
    print(f"Email reminder task submitted with ID: {task.id}")
    
    # Wait for task to execute
    try:
        result = task.get(timeout=30)
        print(f"Email task result: {result}")
    except Exception as e:
        print(f"Task execution error: {e}")

if __name__ == "__main__":
    print("=== CELERY WORKER TEST ===")
    print(f"Current time: {datetime.datetime.now().isoformat()}")
    print("Testing simple task...")
    test_simple_task()
    
    print("\nTesting email reminder task...")
    test_email_task()
    
    print("\nAll tests completed!")
    app_context.pop()