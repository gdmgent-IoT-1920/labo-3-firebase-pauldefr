import firebase from '../../config';
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

const firebase = firebase.firestore();

// LEDs


let color = [0, 0, 0];
let noColor = [10,0,0];

const clearPixels = (event) => {
	event.preventDefault();
	for(let box = 0; box < 64; box ++) {
		const row = Math.floor(box / 8);
		const column = box % 8;
		const checkbox = document.getElementById(`pixel-${row}-${column}`);
		checkbox.checked = false;
		
	}
}

// data

const updateData = (data) => {
	const tempElement = document.getElementById("temperature");
	const humidityElement = document.getElementById("humidity");
	console.log(data);
	tempElement.innerHTML = data.temperature;
	humidityElement.innerHTML = data.humidity;

}

const COLLECTION_DATA = 'data';
const DOCUMENT_DATA = 'metrics';

firestore.collection(COLLECTION_DATA).doc(DOCUMENT_DATA).onSnapshot((doc) => {
	updateData(doc.data());
});