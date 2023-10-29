const timer = document.getElementById('timer')

time = 0
setInterval(() => {
    time++;
    timer.value = time;
}, 1000)