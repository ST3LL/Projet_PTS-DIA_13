const departMinutes = 0
let temps = departMinutes * 60

const timerElement = document.getElementById("timer")

var interval = setInterval(() => {
    let minutes = parseInt(temps / 60, 10)
    let secondes = parseInt(temps % 60, 10)

    minutes = minutes < 10 ? "0" + minutes : minutes
    secondes = secondes < 10 ? "0" + secondes : secondes

    timerElement.innerText = `${minutes}:${secondes}`
    temps = temps >= 6000 ? 6000 : temps + 1
}, 1000)


function reset_timer(){
    temps = departMinutes * 60

    let minutes = parseInt(temps / 60, 10)
    let secondes = parseInt(temps % 60, 10)

    minutes = minutes < 10 ? "0" + minutes : minutes
    secondes = secondes < 10 ? "0" + secondes : secondes

    timerElement.innerText = `${minutes}:${secondes}`
    stop_timer()
    restart_timer()
}

function stop_timer() {
    clearInterval(interval);
}

function restart_timer() {
    interval = setInterval(() => {
        let minutes = parseInt(temps / 60, 10)
        let secondes = parseInt(temps % 60, 10)

        minutes = minutes < 10 ? "0" + minutes : minutes
        secondes = secondes < 10 ? "0" + secondes : secondes

        timerElement.innerText = `${minutes}:${secondes}`
        temps = temps >= 6000 ? 6000 : temps + 1
    }, 1000)
}