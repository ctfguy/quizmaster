<script setup>
import axiosClient from '@/axiosClient';
import NavBar from './NavBar.vue';
import { onMounted, ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

const subjects = ref([])
const search = ref("")

const overlay = ref(false)
const subjectsLoading = ref(true)

const addSubjectMode = ref(true)

const overlaySubjectData = ref({
    subjectName: "",
    subjectDescription: ""
})

const editSubjectId = ref(-1)

const store = useUserStore()

const route = useRouter()

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

function resetOverlayData() {
    overlaySubjectData.value.subjectName = ""
    overlaySubjectData.value.subjectDescription = ""
}

const addNewSubject = () => {
    if (overlaySubjectData.value.subjectName != "") {
        const uri = "/admin/subjects"
        const reqData = {
            "name": overlaySubjectData.value.subjectName,
            "description": overlaySubjectData.value.subjectDescription
        }
        axiosClient.post(uri, reqData).then((response) => {
            resetOverlayData()
            if (response.status == 201) {
                overlay.value = false
                loadSubjects()
                alert("New subject added successfuly")
            } 
        }).catch((error) => {
            alert(error.response.data.error)
        })
    } else {
        alert("Subject name cannot be empty")
    }
}

function prepEditSubject(subjectData) {
    editSubjectId.value = subjectData.id
    overlaySubjectData.value.subjectDescription = subjectData.description
    overlaySubjectData.value.subjectName = subjectData.name
    addSubjectMode.value = false
    overlay.value = true
}

function editSubject() {
    if (overlaySubjectData.value.subjectName != "") {
        const uri = "/admin/subjects/edit/" + editSubjectId.value
        const reqData = {
            "name": overlaySubjectData.value.subjectName,
            "description": overlaySubjectData.value.subjectDescription,
        }
        axiosClient.post(uri, reqData).then((response) => {
            resetOverlayData()
            overlay.value = false
            loadSubjects()
            alert("Subject details edited successfuly")
        }).catch((error) => {
            alert(error.response.data.error)
        })
    } else {
        alert("Subject name cannot be empty")
    }
}

onMounted(() => {
    loadSubjects()
})

</script>

<template>
    <NavBar />
    <v-main>
        <v-overlay v-model="overlay" class="d-flex align-center justify-center" :persistent="true">
            <v-card width="400" class="pa-4">
                <v-card-title>Add a new subject</v-card-title>
                <v-card-text>
                <v-form>
                    <v-text-field
                    label="Subject Name"
                    variant="solo"
                    v-model="overlaySubjectData.subjectName"
                    ></v-text-field>
                    <v-textarea
                    label="Description"
                    variant="solo"
                    v-model="overlaySubjectData.subjectDescription"
                    ></v-textarea>
                    <v-card-actions class="d-flex justify-space-between">
                    <v-btn color="error" @click="overlay = false; resetOverlayData()">Close</v-btn>
                    <v-btn color="success" @click="addSubjectMode ? addNewSubject() : editSubject()">{{ addSubjectMode ? "Add" : "Edit" }}</v-btn>
                    </v-card-actions>
                </v-form>
                </v-card-text>
            </v-card>
        </v-overlay>
        <v-container class="d-flex flex-column justify-center">
            <div class="text-h5 mb-4">Hi there {{ store.name }}</div>
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
                                class="mx-4"
                                icon="mdi-plus"
                                size="small"
                                variant="tonal"
                                @click="addSubjectMode =  true; overlay = true"
                                ></v-btn>
                                
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
                                        <v-btn size="small" @click="prepEditSubject(item.raw)" icon="mdi-pencil" color="error" variant="text"></v-btn>
                                    </v-card-title>
                                    <v-card-text>
                                        {{ item.raw.description }}
                                    </v-card-text>
                                    <v-card-actions>
                                        <v-btn variant="outlined" @click="route.push('/admin/subject/'+item.raw.id)" rounded="xl" size="small" append-icon="mdi-arrow-right">View Chapters</v-btn>
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