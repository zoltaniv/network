document.addEventListener("DOMContentLoaded", function () {
  // Get csrftoken
  const csrftoken = Cookies.get("csrftoken");

  const likeBtns = document.getElementsByClassName("post-like");

  for (let i = 0; i < likeBtns.length; i++) {
    likeBtns[i].onclick = function () {
      fetch("/", {
        method: "PUT",
        headers: { "X-CSRFToken": `${csrftoken}` },
        body: JSON.stringify({ post: this.id }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.deleted) {
            this.firstElementChild.style.color = "white";
            this.lastElementChild.innerHTML = data.likes;
          } else {
            this.firstElementChild.style.color = "lightgreen";
            this.lastElementChild.innerHTML = data.likes;
          }
        })
        .catch((error) => {
          console.log(error);
        });
    };
  }

  if (document.getElementById("subbutton")) {
    const subbutton = document.getElementById("subbutton");

    subbutton.onclick = function () {
      fetch(`${window.location.pathname}`, {
        method: "PUT",
        headers: { "X-CSRFToken": `${csrftoken}` },
      })
        .then((response) => response.json())
        .then((data) => {
          document.getElementById("followers").innerHTML =
            data.user_object_followers;
          if (data.subscription == 0) {
            document.getElementById("subbutton").innerHTML = "Unsubscribe";
          } else {
            document.getElementById("subbutton").innerHTML = "Subscribe";
          }
        })
        .catch((error) => {
          console.log(error);
        });
    };
  }
});
