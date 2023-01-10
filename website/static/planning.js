const WEEK_LENGTH = 24 * 60 * 60 * 1000 * 7; // A week length in ms

// Fetch data
let reservationsDiv = document.querySelector("#reservations");
let reservationsJSON = JSON.parse(reservationsDiv.dataset.reservations).list;

console.log(reservationsJSON);

// Reservation class is used to turn the JSON we fetched into objects
// These objects will then be redisplayed on the planning
class Reservation {
	constructor(id, time, user_id) {
		this.id = id;
		this.time = new Date(time);
		this.user_id = user_id;
	}

	onCurrentWeek() {
		let lastMonday = new Date(); // Creating new date object for today
		lastMonday.setDate(lastMonday.getDate() - (lastMonday.getDay() - 1)); // Setting date to last monday
		lastMonday.setHours(0, 0, 0, 0); // Setting Hour to 00:00:00:00

		const res =
			lastMonday.getTime() <= this.time.getTime() &&
			this.time.getTime() < lastMonday.getTime() + WEEK_LENGTH;
		return res; // true / false
	}
}

let reservations = [];
reservationsJSON.forEach((reservationJSON) => {
	let reservation = new Reservation(
		reservationJSON.id,
		reservationJSON.time,
		reservationJSON.user_id
	);

	reservations.push(reservation);
});

console.log(reservations);

reservations.forEach((reservation) => {
	if(reservation.onCurrentWeek()) {
		const dayNb = reservation.time.getDay();
		const hour = reservation.time.getHours();


	}
});
