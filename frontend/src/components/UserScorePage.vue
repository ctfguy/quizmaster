<script setup>
import axiosClient from '@/axiosClient';
import NavBar from './NavBar.vue';
import { ref } from 'vue';

const scores = ref([])

const headers = [
    {title: 'Subject', key:'subject', sortable: true},
    {title: 'Chapter', key:'chapter', sortable: true},
    {title: 'Attempted ', key:'time_stamp_of_attempt', sortable: true},
    {title: 'Score', key: 'marks_scored', sortable: true}
]

axiosClient.get("/user/scores").then((data) => {
    scores.value = data.data.scores
})

</script>

<template>
    <NavBar />
    <v-main>
        <v-container>
            <div class="text-h5 me-auto mb-4">Your scores</div>
            <v-divider></v-divider>
            <v-data-table
                class="mt-4"
                :headers="headers"
                :items="scores"
                item-key="time_stamp_of_attempt"
                hide-default-footer
            ></v-data-table>
        </v-container>
    </v-main>
</template>