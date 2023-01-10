const WEEK_LENGTH = 604800000;

let reservationsDiv = document.querySelector("#reservations");
let reservationsJSON = JSON.parse(reservationsDiv.dataset.reservations);

console.log(reservationsJSON, "reservations");

class Reservation {
	constructor(id, time, user_id) {
		this.id = id;
		this.time = new Date(time);
		this.user_id = user_id;
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
