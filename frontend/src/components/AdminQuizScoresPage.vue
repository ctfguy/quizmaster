<script setup>
import { ref } from 'vue';
import NavBar from './NavBar.vue';
import { useRoute } from 'vue-router';
import axiosClient from '@/axiosClient';

const route = useRoute()
const quizId = route.params.quizId

const scores = ref([])

const headers = [
    {title: 'Name', value:'user_name'},
    {title: 'Attempted on', value:'time_stamp_of_attempt'},
    {title: 'Score', value: 'marks_scored'}
]

axiosClient.get(`/admin/quiz/${quizId}/scores`).then((data) => {
    scores.value = data.data.scores
    console.log(data.data.scores)
}).catch((error) => {
    console.log(error)
})

</script>

<template>
    <NavBar />
    <v-main>
        <v-container>
            <v-data-table
                :headers="headers"
                :items="scores"
                item-key="time_stamp_of_attempt"
                hide-default-footer
            ></v-data-table>
        </v-container>
    </v-main>
</template>