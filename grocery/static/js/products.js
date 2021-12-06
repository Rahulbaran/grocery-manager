"use strict";

const newProductsForm = document.querySelector(".new__products__form");
const newProductsContainer = document.querySelector(
    ".new__products__fields__container"
);
const newProductBtn = document.querySelector(".new__product__btn");
const addProductBtn = document.querySelector(".add__product__btn");
const productsTable = document.querySelector(".products__table");
const productsMainContainer = document.querySelector(
    ".products--main--container"
);

/* ****************************
 * event handler to add new Product Form
 * ************************** */
newProductBtn.addEventListener("click", () => {
    const newProductInput = `<div class="new__product"><label><span>Product Name</span><input type="text" class="product__name" required placeholder="product name" title="product name should be maximum 200 characters long"></label><label><span>Unit</span><input type="text" class="product__unit" required placeholder="product unit" title="product unit should be maximum 20 characters long"></label><label><span>Price (In Rs.)</span><input type="number" class="product__price" required placeholder="product price" title="product price should be maximum 10 characters long"></label><button type="button" class="new__product__remove__btn btn">Remove</button></div>`;
    newProductsContainer.insertAdjacentHTML("afterbegin", newProductInput);
});

/* ******************************
 * event handler to remove a product form
 * *************************** */
newProductsContainer.addEventListener("click", function (e) {
    const parent =
        e.target.parentNode.className === "new__product" &&
        e.target.localName === "button";
    if (parent) this.removeChild(e.target.parentNode);
});

/* ******************************
 * event handler to make http request for sending new products data
 * *************************** */
newProductsForm.addEventListener("submit", function (e) {
    //1. prevent default submit behaviour
    e.preventDefault();

    //2. Pushing product data in products array
    const newProducts = e.target.children[0].children;
    const products = [];

    for (let i = 0; i < newProducts.length; i++) {
        const grandChildren = newProducts[i].children;
        const product = new Array();
        for (let j = 0; j < grandChildren.length - 1; j++) {
            const input = grandChildren[j].children[1];
            product.push(input.value);
            input.value = "";
        }
        products.push(product);
    }

    //3. Removing product input fields
    const totalChildren = newProducts.length - 1;
    for (let prod = 0; prod < totalChildren; prod++) {
        newProductsContainer.removeChild(newProductsContainer.firstChild);
    }

    //4. post request to send products data
    const url = "/getProducts";
    const init = {
        mode: "same-origin",
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ products: products }),
    };

    fetch(url, init)
        .then(res => {
            if (res.status === 200) {
                res.json().then(res => {
                    const products = res.newProducts;
                    const tableBody = document.querySelector("tbody");

                    products.forEach(prod => {
                        const lastIndex = tableBody.children.length;
                        const newProduct = `<tr id="product--${prod[0]}"><td>${
                            lastIndex + 1
                        }</td><td>${prod[1]}</td><td>${prod[2]}</td><td>${
                            prod[3]
                        }</td><td><button class="product__remove__btn btn">Remove</button></td></tr>`;
                        tableBody.insertAdjacentHTML("beforeend", newProduct);
                    });

                    //display message if some products which we were trying to add, are already in database
                    if (res.alreadyExistProducts) {
                        const msg = `<div class="msg__container info__msg__container"><span>Some products are not added in list since they already exist</span>
                    <button class="msg__hide__btn">&Cross;</button></div>`;
                        productsMainContainer.insertAdjacentHTML(
                            "afterbegin",
                            msg
                        );
                    }
                });
            } else console.error("Did not get the result");
        })
        .catch(() =>
            console.error(
                "Something went wrong while getting making the request"
            )
        );
});

/* *****************************
 * event handler to remove product(s) from the product list
 * ************************** */
productsTable.addEventListener("click", function (e) {
    const removeBtn = e.target.classList.contains("product__remove__btn");

    if (removeBtn) {
        const product = e.target.parentNode.parentNode;
        //1. get the product id
        const productId = product.id.split("--")[1];

        //2. remove product from db
        const init = {
            mode: "same-origin",
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            cache: "default",
            body: JSON.stringify({ id: +productId }),
        };

        fetch("/removeProduct", init)
            .then(res => {
                if (res.status === 200) return;
                else console.error(res);
            })
            .catch(console.error);

        //3. remove product from ui
        this.children[1].removeChild(product);

        //4. update product indexes in ui
        const allProducts = this.children[1].children;
        for (let i = 1; i <= allProducts.length; i++) {
            allProducts[i - 1].firstElementChild.textContent = i;
        }
    }
});

/* ****************************
 * functionality to hide flashed message
 * ************************** */
productsMainContainer.addEventListener("click", function (e) {
    if (e.target.classList.contains("msg__hide__btn")) {
        this.removeChild(e.target.parentNode);
    }
});
