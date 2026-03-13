document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  let isFetching = false;
  async function fetchActivities() {
    if (isFetching) return; // Prevent multiple concurrent calls
    isFetching = true;

    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Build the entire activities list HTML
      let activitiesHtml = "";
      let optionsHtml = '<option value="">-- Select an activity --</option>';

      Object.entries(activities).forEach(([name, details]) => {
        const spotsLeft = details.max_participants - details.participants.length;

        activitiesHtml += `
          <div class="activity-card">
            <h4>${name}</h4>
            <p>${details.description}</p>
            <p><strong>Schedule:</strong> ${details.schedule}</p>
            <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
            <div class="participants-section">
              <strong>Participants:</strong>
              <ul>
                ${details.participants.length > 0 ? details.participants.map(p => `<li>${p} <button class="delete-btn" data-activity="${name}" data-email="${p}">×</button></li>`).join('') : '<li>No participants yet</li>'}
              </ul>
            </div>
          </div>
        `;

        optionsHtml += `<option value="${name}">${name}</option>`;
      });

      // Set the HTML all at once
      activitiesList.innerHTML = activitiesHtml;
      activitySelect.innerHTML = optionsHtml;

    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    } finally {
      isFetching = false;
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        // Refresh the activities list to show the new participant
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();

  // Event listener for delete buttons
  activitiesList.addEventListener('click', async (event) => {
    if (event.target.classList.contains('delete-btn')) {
      const activity = event.target.dataset.activity;
      const email = event.target.dataset.email;

      try {
        const response = await fetch(
          `/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`,
          {
            method: "DELETE",
          }
        );

        if (response.ok) {
          // Refresh the activities list
          fetchActivities();
        } else {
          const result = await response.json();
          alert(result.detail || "Failed to unregister");
        }
      } catch (error) {
        alert("Error unregistering participant");
        console.error("Error:", error);
      }
    }
  });
});
