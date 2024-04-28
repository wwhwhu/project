<template>
  <div class="min-h-screen">
    <div class="container flex flex-col items-center mx-auto px-6 py-10 ">
      <CombinedScatterChart v-if="cars.length > 0" :allCarData="cars" class="mb-10"/>
      <div class="grid grid-cols-2 gap-3">
        <div v-for="car in cars" :key="car.name" class="p-6 bg-white rounded-lg shadow-md mt-6">
          <ScatterChart :carData="car.data" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ScatterChart from '../components/ScatterChart';
import CombinedScatterChart from '../components/CombinedScatterChart';

export default {
  name: 'carPage',
  components: {
    ScatterChart,
    CombinedScatterChart
  },
  data() {
    return {
      cars: []
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      axios.get('http://localhost:3000/cars')
          .then(response => {
            const groupedData = {};
            response.data.forEach(car => {
              if (!groupedData[car.name]) {
                groupedData[car.name] = {
                  name: car.name,
                  data: []
                };
              }
              groupedData[car.name].data.push(car);
            });
            this.cars = Object.values(groupedData);
          })
          .catch(error => {
            console.error('There was an error fetching the cars data:', error);
            alert('Failed to fetch cars data. Please try again later.')
          });
    }
  }
}
</script>

<style>
/* Local styles if necessary */
</style>
