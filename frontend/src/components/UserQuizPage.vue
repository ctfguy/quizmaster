<script setup>
    import axiosClient from '@/axiosClient';
    import { ref } from 'vue';
    import { useRoute } from 'vue-router';
    import NavBar from './NavBar.vue';
import router from '@/router';

    const route = useRoute()
    const quizId = route.params.quizId

    const submitted = ref(false)
    const seconds = ref("00")
    const minutes = ref("00")

    var seconds_left = 0

    const step = ref(1)

    const questions = ref([])

    function submitQuiz() {
        submitted.value = true
        const answers = []
        for (const question of questions.value) {
            answers.push({
                question_id: question.id,
                option: question.option
            })
        }
        const reqBody = {
            "answers": answers
        }
        console.log(reqBody)
        axiosClient.post(`user/quiz/${quizId}/attempt`, reqBody).then((data) => {
            alert("Quiz submitted successfully")
            router.back()
        }).catch((error) => {
            console.log(error)
            submitted.value = false
        })
    }

    function updateTimer() {
        const curMinutes = Math.floor(seconds_left / 60).toString()
        const curSeconds = (seconds_left % 60).toString()
        seconds.value = curSeconds.length == 1 ? "0" + curSeconds : curSeconds
        minutes.value = curMinutes.length == 1 ? "0" + curMinutes : curMinutes
    }

    function startTimer() {
        var interval = setInterval(() => {
            seconds_left--
            updateTimer()
            if (seconds_left == 0) {
                clearInterval(interval)
                if (!submitted.value) {
                    submitQuiz()
                }
            }
        }, 1000)
    }

    axiosClient.get(`/quiz/${quizId}/questions`).then((data) => {
        console.log(data.data)
        questions.value = data.data.questions
        seconds_left = data.data.time_duration * 60
        updateTimer()
        startTimer()
    }).catch((error) => {
        console.log(error)
    })
</script>

<template>
    <NavBar />
    <v-main>
        <v-container v-if="questions.length > 0">
            <div class="d-flex align-center">
                <div class="text-h6 mb-4 my-auto mr-auto">Quiz on</div>
                <div class="text-overline">Time left {{ minutes }}:{{ seconds }}</div>
            </div>
            <v-divider></v-divider>
            <v-card class="mt-6">
                <v-card-title>
                    <div class="text-h6">{{ step + ". " + questions[step-1].question_statement}} </div>
                </v-card-title>
                <v-window v-model="step">
                    <v-window-item v-for="(question, i) in questions" :value="i+1">
                        <v-card-text class="py-0">
                            <v-radio-group v-model="question.option" color="red">
                                <v-radio v-for="(option, i) in question.options" :label="option" :value="i+1"></v-radio>
                            </v-radio-group>
                        </v-card-text>
                    </v-window-item>
                </v-window>
                <v-card-actions class="pt-0">
                    <v-btn
                        v-if="step > 1"
                        variant="text"
                        @click="step--"
                    >
                        Back
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn
                        v-if="step < questions.length"
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
                        :loading="submitted"
                        @click="submitQuiz"
                    >
                        Submit
                    </v-btn>
                </v-card-actions>
                
            </v-card>
    
        </v-container>
    </v-main>
</template>