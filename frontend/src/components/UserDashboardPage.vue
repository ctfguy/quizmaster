<script setup>
import { ref } from 'vue';
import NavBar from './NavBar.vue';
import { useUserStore } from '@/stores/user';
import axiosClient from '@/axiosClient';
import router from '@/router';

const subjectsLoading = ref(true)
const subjects = ref([])

const search = ref("")

const store = useUserStore()

function loadSubjects() {
    subjectsLoading.value = true
    axiosClient.get('/quiz/subjects').then((data) => {
        subjects.value = data.data.subjects
        setInterval(() => {
            subjectsLoading.value = false
        }, 800)
    }).catch((error) => {
    console.log(error)
    })
}

loadSubjects()
</script>

<template>
    <NavBar />
    <v-main>
        <v-container class="d-flex flex-column justify-center">
            <div class="d-flex mb-4 ">
                <div class="text-h5 me-auto">Hi there {{ store.name }}</div>
                <v-btn color="primary" variant="outlined" to="/user/scores">View scores</v-btn>
            </div>
            <v-divider></v-divider>
            <v-card class="mt-4">
                <v-data-iterator :items="subjects" :items-per-page="4" :search="search" :loading="subjectsLoading">
                    <template v-slot:header="{ page, pageCount, prevPage, nextPage }">
                        <v-toolbar class="px-2">
                            <v-toolbar-title>Subjects</v-toolbar-title>
                            <v-text-field
                                v-model="search"
                                density="comfortable"
                                placeholder="Search"
                                prepend-inner-icon="mdi-magnify"
                                style="max-width: 300px;"
                                variant="solo"
                                clearable
                                hide-details
                            ></v-text-field>
                            <div class="ml-2 d-inline-flex">
                                <v-btn
                                :disabled="page === 1"
                                class="me-2"
                                icon="mdi-arrow-left"
                                size="small"
                                variant="tonal"
                                @click="prevPage"
                                ></v-btn>
                                <v-btn
                                :disabled="page === pageCount"
                                icon="mdi-arrow-right"
                                size="small"
                                variant="tonal"
                                @click="nextPage"
                                ></v-btn>
                            </div>
                        </v-toolbar>
                        
                    </template>
                    <template v-slot:default="{ items }">
                        <v-row class="my-2 px-6">
                            <v-col 
                                v-for="item in items"
                                cols="12"
                                sm="6"
                                xl="3">
                                <v-card variant="tonal" class="pa-3">
                                    <v-card-title>
                                        {{ item.raw.name }}
                                    </v-card-title>
                                    <v-card-text>
                                        {{ item.raw.description }}
                                    </v-card-text>
                                    <v-card-actions>
                                        <v-btn variant="outlined" @click="router.push('/user/subject/'+item.raw.id)" rounded="xl" size="small" append-icon="mdi-arrow-right">View Chapters</v-btn>
                                    </v-card-actions>
                                </v-card>
                            </v-col>
                        </v-row>
                    </template>
                    <template v-slot:loader>
                        <v-row class="pa-4">
                            <v-col
                                v-for="(_, k) in [0, 1, 2, 3]"
                                :key="k"
                                cols="12"
                                sm="6"
                                xl="3"
                            >
                            <v-skeleton-loader
                                class="border pa-2"
                                type="heading, text, chip"
                            ></v-skeleton-loader>
                            </v-col>
                        </v-row>
                    </template>
                </v-data-iterator>
            </v-card>
        </v-container>
    </v-main>
</template>