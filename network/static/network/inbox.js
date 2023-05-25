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
        if (subbutton.textContent == 'Subscribe') {
          fetch(`${window.location.pathname}`, {
            method: "PUT",
            headers: { "X-CSRFToken": `${csrftoken}` },
            body: JSON.stringify({ subscribe: true }),
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.subscription == 0) {
                document.getElementById("followers").innerHTML =
                  data.user_object_followers;
                document.getElementById("subbutton").innerHTML = "Unsubscribe";
              }
            })
            .catch((error) => {
              console.log(error);
            });
        } else {
          fetch(`${window.location.pathname}`, {
            method: "PUT",
            headers: { "X-CSRFToken": `${csrftoken}` },
            body: JSON.stringify({ subscribe: false }),
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.subscription == 1) {
                document.getElementById("followers").innerHTML =
                  data.user_object_followers;
                document.getElementById("subbutton").innerHTML = "Subscribe";
              }
            })
            .catch((error) => {
              console.log(error);
            });
        }
      };
    }
});
