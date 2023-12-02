<template>
    <div class="visual-component">
      <!-- Left Section -->
      <div class="left-section">
        <img :src="require('I:/desktop/UI/Backen/data/' + origin_path)" alt="Left Image 1" class="left-image">
        <img :src="leftImage2" alt="Left Image 2" class="left-image">
      </div>
  
      <!-- Right Section -->
      <div class="right-section">
        <div class="scrollable-info">
          <div v-for="(info, index) in infoList" :key="index" class="info-item">
            <div class="info-images">
                <span  class="image-index">{{ index + 1 }}</span>
                <img :src="require('I:/desktop/UI/Backen/data/'+info.person)" class="info-image">
                <img :src="require('I:/desktop/UI/Backen/data/'+info.object)" class="info-image">
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        leftImage1: require('@/assets/g1.png'),
        leftImage2: require('@/assets/g1.png'),
        data_dir: 'I:/desktop/Backen/data/',
        result: {},
        origin_path: '',
        infoList: []
      };
    },
    methods: {
      fetchData() {
        axios.get('http://localhost:5000/get_info_list')
          .then(response => {
            this.result = response.data.result;
            this.origin_path = response.data.result.origin_path;
            this.infoList = response.data.result.info_list;
            this.error = null;
            console.log(this.infoList);
          })
          .catch(error => {
            console.error('Error fetching infoList:', error);
          });
      },
    },
    mounted() {
      this.fetchData();
      setInterval(() => {
        this.fetchData();
      }, 1000);
    },
  };
  </script>



<style scoped>
.visual-component {
display: flex;
max-width: 100vw;
max-height: 80vh;
margin: auto;
}

.left-section {
width:70%;
display: flex;
flex-direction: column;
justify-content: center;
align-items: center;
}

.right-section {
width: 30%;
/* display: flex; */
overflow-y: auto;
}

.left-image {
height: 50%; 
margin-top:2%;
}

.scrollable-info {
height: 100%;
padding: 20px;
}

.info-item {
height: 24%;
margin-bottom: 0px;
}

.image-index {
    display: inline-block;
    padding: 5px 10px;
    background-color: #3498db; /* 设置背景颜色 */
    color: #fff; /* 设置文字颜色 */
    border-radius: 5px; /* 设置圆角 */
    margin-right: 5px; /* 设置右侧间距 */
    font-size: 32px; /* 设置字体大小 */
    text-align: center; /* 设置文本居中 */
    line-height: 1.5; /* 设置行高，使得垂直居中 */
}

.info-image {
    display: flex;
    height:100%;
    width: 100%;
    /* max-height: 100px; */
    margin-right: 30px;
}

.info-images {
    display: flex;
    height: 100%;
    width: auto;
    margin: 10px;
    /* flex-wrap: nowrap; */
}
</style>
  