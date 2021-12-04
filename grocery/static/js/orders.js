"use strict";

const newOrdersWrapper = document.querySelector(
    ".new__orders__fields__container"
);
const ordersForm = document.querySelector(".new__orders__form");
const customerNameField = document.querySelector(
    ".customer__name__field input"
);
const tableBody = document.querySelector("tbody");

/**************************
 * event handler to remove newOrder fields
 * *********************** */
newOrdersWrapper.addEventListener("click", function (e) {
    const orderField =
        e.target.parentNode.className === "new__order__fields" &&
        e.target.localName === "button";
    if (orderField) this.removeChild(e.target.parentNode);
});

// Function to make http request for getting unit of the selected product
const getProductName = function (prodInput) {
    const value = prodInput.value;

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/getProductDetails");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.responseType = "json";
    xhr.onload = function () {
        const unit = xhr.response["unit"];
        if (unit) {
            prodInput.parentNode.nextElementSibling.children[1].value = unit;

            //updating the total price if product quantity exist
            const product = prodInput.parentNode.parentNode;
            const quantity = product.children[2].children[1].value;
            if (quantity) {
                let totalPrice = product.children[3].children[1];
                totalPrice.value = Number(quantity) * xhr.response["price"];
            }
        }
    };

    xhr.onerror = () => console.error("Internal Server Error");
    xhr.send(JSON.stringify({ name: value }));
};

//Function to make http request for calculating total price
const calcTotalPrice = prodInput => {
    const prodQuan = Number(prodInput.value);
    const prodName =
        prodInput.parentNode.parentNode.children[0].children[1].value;
    const prodObj = { name: prodName };

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/getProductDetails");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.responseType = "json";
    xhr.onload = () => {
        if (xhr.status === 200) {
            const prodPrice = xhr.response["price"];
            if (prodPrice)
                prodInput.parentNode.nextElementSibling.children[1].value =
                    prodPrice * prodQuan;
        } else {
            console.error(xhr.statusText);
        }
    };
    xhr.onerror = () => console.error("Internal Server Error");
    xhr.send(JSON.stringify(prodObj));
};

/*****************************
 * event handler for orders form submission
 * ************************** */
ordersForm.addEventListener("submit", e => {
    //1. Preventing form default submission behavior
    e.preventDefault();

    //2. storing order details in a suitable data structure and empting the input fields
    const allOrders = newOrdersWrapper.children;
    const ordersData = [];

    for (let i = 0; i < allOrders.length; i++) {
        const fields = allOrders[i].children;
        const orderData = new Array();

        for (let j = 0; j < fields.length - 1; j++) {
            orderData.push(fields[j].children[1].value);
            if (j !== 0) fields[j].children[1].value = "";
            else fields[j].children[1].value = "Product name";
        }
        ordersData.push(orderData);
    }
    const ordersJSON = JSON.stringify({
        customer: customerNameField.value,
        orders: ordersData,
    });
    customerNameField.value = "";

    //3. Removing orders input fields
    for (let index = 0; index < allOrders.length - 1; index++) {
        newOrdersWrapper.removeChild(allOrders[index]);
    }

    //4. making http request to send and recieve json data
    const httpReq = async () => {
        const init = {
            mode: "same-origin",
            cache: "no-cache",
            method: "POST",
            body: ordersJSON,
            headers: { "Content-Type": "application/json" },
        };
        const response = await fetch("/getOrders", init);

        if (response.status === 200) {
            return response.json();
        } else {
            throw Error("Did not get the expected result");
        }
    };
    httpReq()
        .then(res => {
            const newOrders = res["orders"];

            newOrders.forEach(ord => {
                const lastIndex = tableBody.children.length;

                const orderHtml = `<tr id="order--${ord[0]}"><td>${
                    lastIndex + 1
                }</td><td>${ord[1]}</td><td>${ord[0]}</td><td>${ord[2]}</td>
            <td>${ord[3]} (${ord[4]})</td><td>${ord[5]}</td><td>${
                    ord[6]
                }</td><td><button class="order__remove__btn btn">Remove</button></td></tr>`;
                tableBody.insertAdjacentHTML("beforeend", orderHtml);
            });
        })
        .catch(console.error);
});

/**************************
 * event handler to delete orders from ui and database
 * *************************/
tableBody.addEventListener("click", function (e) {
    const orderRemoveBtn = e.target.classList.contains("order__remove__btn");

    if (orderRemoveBtn) {
        //1. Get order id
        const order_id = e.target.parentNode.parentNode.id.split("--")[1];

        //2. http request to remove the order from database
        const http = async () => {
            const init = {
                mode: "same-origin",
                method: "post",
                body: JSON.stringify({ id: +order_id }),
                headers: {
                    "Content-Type": "application/json",
                },
                cache: "default",
            };
            const response = await fetch("/removeOrder", init);

            if (response.status === 200) return response.text();
            else throw Error("Did not get the expected result");
        };

        http()
            .then(res => console.log(res))
            .catch(console.error);

        //3. Remove the order from UI
        this.removeChild(e.target.parentNode.parentNode);

        //4. Update order indexes in UI
        const allOrders = this.children;
        for (let index = 0; index < allOrders.length; index++) {
            allOrders[index].children[0].textContent = index + 1;
        }
    }
});
