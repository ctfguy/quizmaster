<script setup>
import { useRoute } from 'vue-router';
import NavBar from './NavBar.vue';
import axiosClient from '@/axiosClient';
import { ref } from 'vue';

const route = useRoute()
const subjectId = route.params.subjectId
const subjectName = ref("")
const loading = ref(true)
const chapters = ref([])

axiosClient.get(`/user/subject/${subjectId}/chapters`).then((data) => {
    console.log(data.data.chapters)
    chapters.value = data.data.chapters
    subjectName.value = data.data.subject + " - "
    loading.value = false
}).catch((error) => {
    console.log(error)
})

function isQuizAvailable(date_of_quiz) {
    const start_date = new Date(date_of_quiz)
    const current_date = new Date()
    return (current_date - start_date) < 0
}

</script>

<template>
    <NavBar />
    <v-main>
        <v-container>
            <div class="d-flex">
                <div class="text-h6 mb-4 me-auto">{{ subjectName }} Chapters</div>
            </div>
            <v-divider></v-divider>
            <v-skeleton-loader
                class="mt-4"
                v-if="loading"
                type="list-item-two-line"
            ></v-skeleton-loader>
            <v-expansion-panels class="mt-4" v-else>
                <v-expansion-panel v-for="(chapter, i) in chapters">
                    <v-expansion-panel-title>
                        <v-row>
                            <v-col class="text-subtitle text-uppercase d-flex align-self-center" cols="6" md="4">{{ (1+i).toString() + ". " + chapter.name }}</v-col>
                            <v-divider vertical></v-divider>
                            <v-col class="text-caption d-flex align-self-center" cols="6" md="8">
                                {{ chapter.description }}
                            </v-col>
                        </v-row>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <v-row>
                            <v-col class="d-flex justify-center align-center" cols="6">
                                <div class="d-inline text-primary" >duration: </div> {{ " " + chapter.time_duration + " mins"}}  
                            </v-col>
                            <v-col v-if="isQuizAvailable(chapter.date_of_quiz)" class="d-flex justify-center align-center" cols="6">
                                <div class="d-inline text-primary">starts: </div> {{ " " + new Date(chapter.date_of_quiz).toLocaleDateString() }}
                            </v-col>
                            <v-col v-else cols="6" class="d-flex justify-center align-center" >
                                <div v-if="chapter.attempted" class="d-inline "><span class="text-success">Your Score: </span>{{ chapter.score.total_scored }} / {{ chapter.score.total_possible }}</div>
                                <v-btn v-else v-bind:to="`/user/quiz/${chapter.quiz_id}`" color="green" size="small">Attempt</v-btn>
                            </v-col>
                        </v-row>
                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-container>
    </v-main>

</template>