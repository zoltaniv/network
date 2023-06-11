document.addEventListener("DOMContentLoaded", function () {
  // Get csrftoken
  const csrftoken = Cookies.get("csrftoken");

  const likeBtns = document.getElementsByClassName("post-like");

  for (let i = 0; i < likeBtns.length; i++) {
    likeBtns[i].onclick = function () {
      fetch("/", {
        method: "PUT",
        headers: { "X-CSRFToken": `${csrftoken}` },
        body: JSON.stringify({
          post: this.id,
          likeButton: true,
          saveChangesButton: false
        }),
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

  // Create edit function ============================================================================
  if (document.querySelector(".post-edit")) {
    const editButtons = document.getElementsByClassName("post-edit");
    for (let i = 0; i < editButtons.length; i++) {
      editButtons[i].onclick = function () {
        const textarea = document.createElement("textarea");
        textarea.className = "edit-area";
        textarea.innerHTML = this.parentNode.childNodes[3].textContent;
        this.parentNode.childNodes[3].appendChild(textarea);
        this.parentNode.childNodes[3].firstChild.remove();
        const saveButton = this.nextElementSibling;
        saveButton.style.display = "block";
        this.style.display = "none";
        saveButton.onclick = function () {
          fetch("/", {
            method: "PUT",
            headers: { "X-CSRFToken": `${csrftoken}` },
            body: JSON.stringify({
              post: this.parentNode.childNodes[7].id,
              text: textarea.value,
              saveChangesButton: true,
              likeButton: false,
            }),
          })
            .then((response) => response.json())
            .then((post) => {
              if (post["text"]) {
                const textNode = document.createTextNode(post.text);
                this.parentNode.childNodes[3].firstElementChild.remove();
                this.parentNode.childNodes[3].appendChild(textNode);
                this.style.display = "none";
                this.previousElementSibling.style.display = "block";
              }
            });
        };
      };
    }
  }
});
