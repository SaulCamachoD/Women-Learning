function success(data, textStatus){
    console.log(textStatus);
    console.log(data);
    if (textStatus === "success"){
        let responseDiv = document.querySelector("#response");
        let books = data.items;
        let text = "";
        for (let i = 0; i < books.length; i++){
            let image = books[i].volumeInfo.imageLinks.thumbnail;
            text += `Título: ${books[i].volumeInfo.title}<br> Autores: ${books[i].volumeInfo.authors} <br> <img src= "${image}"> <br> Link: ${books[i].volumeInfo.infoLink} <br> <br>  `
        }

        responseDiv.innerHTML = text;
    }
}

function searchGoogleBooks(){
    let input = document.querySelector("input");
    let searchTerms = input.value;
    let maxResults = 10;
    let URL = `https://www.googleapis.com/books/v1/volumes?q=${searchTerms}&maxResults=${maxResults}`;
    $.get({
        url: URL, 
        success: function(response) {
            let booksContainer = document.querySelector("#books-container");
            booksContainer.innerHTML = ""; // Limpiar el contenedor

            response.items.forEach(function(book) {
                // Crear una caja para cada libro
                let bookBox = document.createElement("div");
                bookBox.classList.add("book-box");

                // Agregar la información del libro a la caja
                let title = document.createElement("h2");
                title.innerText = book.volumeInfo.title;
                bookBox.appendChild(title);

                let author = document.createElement("p");
                author.innerText = `Autor: ${book.volumeInfo.authors.join(", ")}`;
                bookBox.appendChild(author);

                // Agregar la imagen de portada a la caja
                let coverImage = document.createElement("img");
                let imageLink = book.volumeInfo.imageLinks.thumbnail;
                coverImage.setAttribute("src", imageLink);
                bookBox.appendChild(coverImage);

                let link = document.createElement("a");
                link.setAttribute("href", book.volumeInfo.infoLink);
                link.innerText = "Ver más";
                bookBox.appendChild(link);

                // Agregar la caja al contenedor
                booksContainer.appendChild(bookBox);
            });
        } 
    });
}
