<script setup>
import NavBar from './NavBar.vue';
import { ref } from 'vue';


var loaded = ref(true)

</script>

<template>
    <NavBar />
    <v-main>
        <v-container v-if="loaded" class="h-100 d-flex flex-column justify-center align-center text-center" max-width="800">
            <div class="text-h2 pa-2">Welcome to the quiz app</div>
            <div class="text-subtitle-1 pa-2">Boost your knowledge with fun and interactive quizzes! Choose your favorite
                subjects, challenge yourself, and track your progress—all in one easy-to-use platform. Start learning today!
            </div>
            <v-container class="d-flex justify-center ga-4">
                <v-btn to="/login" color="primary">Sign In</v-btn>
                <v-btn to="/register" color="primary">Sign Up</v-btn>
            </v-container>
        </v-container>
        <v-container v-else class="h-100 d-flex flex-column justify-center align-center text-center">
            <v-progress-circular
                indeterminate
            ></v-progress-circular>
        </v-container>
    </v-main>
</template>