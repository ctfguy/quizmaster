<script setup>
    import { onMounted, ref } from 'vue'
    import NavBar from './NavBar.vue'
    import { useRoute } from 'vue-router'
    import axiosClient from '@/axiosClient'
    import router from '@/router'
    const route = useRoute()
    const loading = ref(false)
    const subjectId = route.params.subjectId
    const step = ref(1)
    const chapter = ref({
        name: '',
        description: "",
        date_of_quiz: "",
        time_duration: 0,
    })
    const questions = ref([
        {
            question_statement: "",
            option1: "",
            option2: "",
            option3: "",
            option4: "",
            correct_option: 1,
        },
    ])

    function addNewQuestion() {
        questions.value.push({
            question_statement: "",
            option1: "",
            option2: "",
            option3: "",
            option4: "",
            correct_option: 1,
        })
    }

    function addChapter() {
        var i = 1
        if (chapter.value.name == "" || chapter.value.date_of_quiz == "" || chapter.value.time_duration == 0) {
            alert("Chapter details cannot be empty")
            step.value = i++
            return
        }
        for (const question of questions.value) {
            if (question.question_statement == "" || 
                    question.option1 == "" ||
                    question.option2 == "" ||
                    question.option3 == "" ||
                    question.option4 == "") {
                alert("Question details cannot be empty")
                step.value = i
                return
            }
            i++
        }
        const questionsList = []
        for (const {question_statement, option1, option2, option3, option4, correct_option} of questions.value) {
            questionsList.push({question_statement,
                                option1,
                                option2,
                                option3,
                                option4,
                                correct_option})
        }
        const reqBody = {
            "chapter": {
                "name": chapter.value.name,
                "description": chapter.value.description
            },
            "quiz": {
                "date_of_quiz": new Date(chapter.value.date_of_quiz).toISOString(),
                "time_duration": chapter.value.time_duration
            },
            "questions": questionsList
        }
        axiosClient.post(`/admin/subjects/${subjectId}/complete-chapter`, reqBody).then((res) => {
            alert("Successfully added the new chapter")
            router.replace(`/admin/subject/${subjectId}`)
        }).catch((error) => {
            console.log(error)
        })
    }
</script>

<template>
    <NavBar />
    <v-main>
        <v-container>
            <v-card>
                <v-card-title>
                    <div v-if="step == 1" class="text-h6">Chapter details</div>
                    <div v-else class="text-h6">Question {{ step-1 }}</div>
                </v-card-title>
                <v-window v-model="step">
                    <v-window-item :value="1">
                        <v-card-text>
                            <v-text-field v-model="chapter.name" label="Chapter Name" variant="outlined" :disabled="loading"></v-text-field>
                            <v-textarea v-model="chapter.description" label="Chapter Description" variant="outlined" :disabled="loading"></v-textarea>
                            <v-text-field v-model="chapter.date_of_quiz" label="Quiz Start Date" type="date" variant="outlined" :disabled="loading"></v-text-field>
                            <v-text-field v-model="chapter.time_duration" label="Quiz Duration (in minutes)" type="number" variant="outlined" :disabled="loading"></v-text-field>
                        </v-card-text>
                    </v-window-item>
    
                    <v-window-item v-for="(question, i) in questions" :value="i+2">
                        <v-card-text>
                            <v-textarea v-model="question.question_statement" label="Question Statement" variant="outlined" :disabled="loading" rows="2"></v-textarea>
                            <v-text-field v-model="question.option1" label="Option 1" variant="outlined" :disabled="loading"></v-text-field>
                            <v-text-field v-model="question.option2" label="Option 2" variant="outlined" :disabled="loading"></v-text-field>
                            <v-text-field v-model="question.option3" label="Option 3" variant="outlined" :disabled="loading"></v-text-field>
                            <v-text-field v-model="question.option4" label="Option 4" variant="outlined" :disabled="loading"></v-text-field>
                            <v-select v-model="question.correct_option" :items="[1, 2, 3, 4]" label="Correct Answer" variant="outlined" :disabled="loading"></v-select>
                        </v-card-text>
                    </v-window-item>
                </v-window>
                <v-card-actions>
                    <v-btn
                        v-if="step > 1"
                        variant="text"
                        @click="step--"
                    >
                        Back
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn
                        v-if="step == questions.length + 1"
                        color="primary"
                        variant="text"
                        @click="addNewQuestion"
                    >
                        Add Question
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn
                        v-if="step < questions.length + 1"
                        color="primary"
                        variant="text"
                        @click="step++"
                    >
                        Next
                    </v-btn>
                    <v-btn 
                        v-else
                        color="success"
                        variant="flat"
                        @click="addChapter"
                        :loading="loading"
                    >
                        Submit
                    </v-btn>
                </v-card-actions>
                
            </v-card>
    
            
        </v-container>
    </v-main>
</template>