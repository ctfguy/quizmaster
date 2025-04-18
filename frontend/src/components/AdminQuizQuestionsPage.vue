<script setup>
import { ref } from 'vue';
import NavBar from './NavBar.vue';
import axiosClient from '@/axiosClient';
import { useRoute } from 'vue-router';

const questions = ref([])

const route = useRoute()
const quizId = route.params.quizId

var quesList = []

function loadQuestions() {
    axiosClient.get(`/quiz/${quizId}/questions`).then((data) => {
        quesList = []
        for (const question of data.data.questions) {
            quesList.push({...question, "edit": false})
        }
        questions.value = structuredClone(quesList)
        console.log(quesList)
    }).catch((error) => {
        console.log(error)
    })
}
loadQuestions()

function resetQuestion(index) {
    questions.value[index] = structuredClone(quesList[index])
}

function editQuestion(index) {
    axiosClient.post(`/admin/questions/edit/${questions.value[index].id}`, {
        "question_statement": questions.value[index].question_statement,
        "correct_option": questions.value[index].correct_option,
        "option1": questions.value[index].options[0],
        "option2": questions.value[index].options[1],
        "option3": questions.value[index].options[2],
        "option4": questions.value[index].options[3],
    }).then(() => {
        questions.value[index].edit=false
        loadQuestions()
        alert("Question edited successfully")
    }).catch((error) => {
        alert(error.response.data.error)
    })
}

</script>

<template>
    <NavBar />
    <v-main>
        <v-container>
            <div class="text-h6 me-auto mb-4">Questions</div>
            <v-divider></v-divider>
            <v-card v-for="(question, i) in questions" class="my-4">
                <v-card-title class="mb-2 d-flex">
                    <div class="text-button me-auto d-inline">Question {{ i + 1 }}</div>
                    <div v-if="question.edit">
                        <v-btn icon="mdi-close-thick" color="red" variant="text" size="small" @click="resetQuestion(i)"></v-btn>
                        <v-btn icon="mdi-check-bold" color="green" variant="text" size="small" @click="editQuestion(i)"></v-btn>
                    </div>
                    <div v-else>
                        <v-btn icon="mdi-pencil" color="primary" variant="text" size="small" @click="question.edit=true"></v-btn>
                    </div>
                </v-card-title>
                <v-card-text>
                    <v-textarea v-model="question.question_statement" label="Question Statement" variant="outlined" :disabled="!question.edit" rows="2"></v-textarea>
                    <v-text-field  v-model="question.options[0]" label="Option 1" variant="outlined" :disabled="!question.edit"></v-text-field>
                    <v-text-field  v-model="question.options[1]" label="Option 2" variant="outlined" :disabled="!question.edit"></v-text-field>
                    <v-text-field v-model="question.options[2]" label="Option 3" variant="outlined" :disabled="!question.edit"></v-text-field>
                    <v-text-field v-model="question.options[3]" label="Option 4" variant="outlined" :disabled="!question.edit"></v-text-field>
                    <v-select v-model="question.correct_option" :items="[1, 2, 3, 4]" label="Correct Answer" variant="outlined" :disabled="!question.edit"></v-select>
                </v-card-text>
            </v-card>
        </v-container>
    </v-main>
</template>