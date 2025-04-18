<script setup>
import { useRoute } from 'vue-router';
import NavBar from './NavBar.vue';
import axiosClient from '@/axiosClient';
import { ref } from 'vue';

const route = useRoute()
const subjectId = route.params.subjectId
const newChapterRoute = `/admin/subject/${subjectId}/chapter/new`

const overlay = ref(false)

const editChapter = ref({
    "name": "",
    "desciption": "",
    "id": -1,
    "quiz_id": -1,
    "time_duration": "",
    "date_of_quiz": ""
})

const chapters = ref([])
const loading = ref(true)

function loadChapters() {
    axiosClient.get(`/quiz/subjects/${subjectId}/chapters`).then((res) => {
        chapters.value = res.data.chapters
        loading.value = false
    }).catch((e) => {
        console.log(e)
    })
}

loadChapters()

function showEditOverlay(chapter) {
    const startDate = new Date(chapter.date_of_quiz).toISOString().substring(0, 10)
    editChapter.value.name = chapter.name
    editChapter.value.desciption = chapter.description
    editChapter.value.id = chapter.id
    editChapter.value.quiz_id = chapter.quiz_id
    editChapter.value.time_duration = chapter.time_duration
    editChapter.value.date_of_quiz = startDate
    overlay.value = true
}

function resetOverlayData() {
    editChapter.value = {
        "name": "",
        "desciption": "",
        "id": -1,
        "quiz_id": -1,
        "time_duration": "",
        "date_of_quiz": ""
    }
}

function editSubject() {
    axiosClient.post(`/admin/chapters/edit/${editChapter.value.id}`, {
        "name": editChapter.value.name,
        "description": editChapter.value.desciption,
        "quiz": {
            "date_of_quiz": new Date(editChapter.value.date_of_quiz).toISOString(),
            "time_duration": editChapter.value.time_duration
        }
    }).then((data) => {
        alert("Chapter edited")
        resetOverlayData()
        loadChapters()
        overlay.value = false
    }).catch((error) => {
        console.log(error.response.data.error)
    })
}

</script>

<template>
    <NavBar />
    <v-main>
        <v-overlay v-model="overlay" class="d-flex align-center justify-center" :persistent="true">
            <v-card width="400" class="pa-4">
                <v-card-title>Edit chapter</v-card-title>
                <v-card-text>
                <v-form>
                    <v-text-field
                    label="Chapter Name"
                    variant="solo"
                    v-model="editChapter.name"
                    ></v-text-field>
                    <v-textarea
                    label="Description"
                    variant="solo"
                    v-model="editChapter.desciption"
                    ></v-textarea>
                    <v-text-field
                    label="Quiz Duration"
                    variant="solo"
                    type="number"
                    v-model="editChapter.time_duration"
                    ></v-text-field>
                    <v-text-field
                    label="Quiz Start Date"
                    variant="solo"
                    type="date"
                    v-model="editChapter.date_of_quiz"
                    ></v-text-field>
                    <v-card-actions class="d-flex justify-space-between">
                    <v-btn color="error" @click="overlay = false; resetOverlayData()">Close</v-btn>
                    <v-btn color="success" @click="editSubject">Edit</v-btn>
                    </v-card-actions>
                </v-form>
                </v-card-text>
            </v-card>
        </v-overlay>
        <v-container>
            <div class="d-flex">
                <div class="text-h6 mb-4 me-auto">Chapters</div>
                <v-btn variant="text" :to="newChapterRoute" color="success">Add Chapter</v-btn>
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
                            <v-col class="d-flex justify-center align-center" cols="6" md="3">
                                <div class="d-inline text-primary">starts: </div> {{ " " + new Date(chapter.date_of_quiz).toLocaleDateString() }}
                            </v-col>
                            <v-col class="d-flex justify-center align-center" cols="6" md="3">
                                <div class="d-inline text-primary" >duration: </div> {{ " " + chapter.time_duration + " mins"}}  
                            </v-col>
                            <v-col class="d-flex justify-center align-center" cols="6" sm="4" md="2">
                                <v-btn size="small" color="primary" variant="tonal" :to="`/admin/quiz/${chapter.quiz_id}/scores`">User Scores</v-btn>
                            </v-col>
                            <v-col class="d-flex justify-center align-center" cols="6" sm="4" md="2">
                                <v-btn size="small" color="primary" variant="tonal" @click="showEditOverlay(chapter)">Edit Chapter</v-btn>
                            </v-col>
                            <v-col class="d-flex justify-center align-center" cols="12" sm="4" md="2">
                                <v-btn size="small" color="primary" variant="tonal" :to="`/admin/quiz/${chapter.quiz_id}/questions`">Questions</v-btn>
                            </v-col>
                        </v-row>
                    </v-expansion-panel-text>
                </v-expansion-panel>
        </v-expansion-panels>
        </v-container>
    </v-main>
</template>