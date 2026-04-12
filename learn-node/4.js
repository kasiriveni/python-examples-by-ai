//make api call https://jsonplaceholder.typicode.com/posts/1
import fetch from "node-fetch";

fetch("https://jsonplaceholder.typicode.com/posts/1")
  .then((response) => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error(`Failed to fetch data: ${response.status}`);
    }
  })
  .then((data) => console.log(data))
  .catch((error) => console.error("Error:", error));
