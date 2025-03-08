async function generateItinerary() {
    const interest = document.getElementById("interest").value;
    const budget = document.getElementById("budget").value;
    const destination = document.getElementById("destination").value;
    const from_date = document.getElementById("from_date").value;
    const to_date = document.getElementById("to_date").value;
    const itinerary = document.getElementById("itinerary");

    if (!interest || !budget || !destination || !fromDate || !toDate) {
        itinerary.innerHTML = "Please enter all details (Interest, Budget, Destination, Dates).";
        return;
    }

    try {
        const response = await fetch("/generate-itinerary", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                interest: interest,
                budget: budget,
                destination: destination,
                from_date: from_date,
                to_date: to_date
            }),
        });

        const data = await response.json();
        itinerary.innerHTML = data.result || "Error generating itinerary.";
    } catch (error) {
        itinerary.innerHTML = "Something went wrong. Try again!";
    }

    itinerary.classList.remove("hidden");
}

async function showAttractions() {
    const destination = document.getElementById("destination").value;
    const recommendations = document.getElementById("recommendations");

    if (!destination) {
        recommendations.innerHTML = "Enter a destination first!";
        return;
    }

    const prompt = `List top tourist attractions and must-visit places in ${destination}.`;

    try {
        const response = await fetch("/get-nearby-attractions", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ destination: destination }),
        });

        const data = await response.json();
        recommendations.innerHTML = data.result || "No attractions found.";
    } catch (error) {
        recommendations.innerHTML = "Error fetching attractions.";
    }

    recommendations.classList.remove("hidden");
}
