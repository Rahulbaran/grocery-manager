"use strict";

/* *******************************
 * Functionality related with infinite scrolling
 * ***************************** */
const loadingSpinner = document.querySelector(".loading__spinner");
const spinnerContainer = document.querySelector(".loading__spinner__container");
const tableBody = document.querySelector(".order__table tbody");
const totalAmount = document.querySelector("tfoot td span");
const firstOrder = document.querySelector(".order__table tbody tr:first-child");
let counter = 20;

//function to load products by making http request
const loadOrders = entries => {
    if (entries[0].isIntersecting) {
        //making http request to recive the furthur orders
        const httpReq = async counter => {
            const url = `/loadOrders?c=${counter}`;
            const init = {
                mode: "same-origin",
                method: "get",
                cache: "no-cache",
            };

            const response = await fetch(url, init);

            if (response.status === 200) {
                return await response.json();
            } else {
                throw Error("Did not get the expected response");
            }
        };
        httpReq(counter)
            .then(res => {
                if (!res["orders"].length) {
                    spinnerContainer.removeChild(
                        spinnerContainer.firstElementChild
                    );
                    const noMorePara = document.createElement("p");
                    noMorePara.setAttribute("class", "noMoreOrder");
                    noMorePara.textContent = "No more Orders";
                    spinnerContainer.append(noMorePara);

                    observer.unobserve(loadingSpinner);
                    return;
                }

                for (let loadOrder of res["orders"]) {
                    //last order index
                    const lastIndex = document.querySelector(
                        ".order__table tbody tr:last-child td:first-child"
                    ).textContent;

                    const orderHtml = firstOrder.cloneNode(true);
                    const orderData = orderHtml.children;

                    orderData[0].textContent = +lastIndex + 1;
                    orderData[1].textContent = loadOrder["customer"];
                    orderData[2].textContent = loadOrder["date"];
                    orderData[3].textContent = loadOrder["total"];

                    tableBody.appendChild(orderHtml);
                }
                counter += 20;
                const earlierTotal = Number(totalAmount.textContent);
                totalAmount.textContent = `${res["totalPrice"] + earlierTotal}`;
            })
            .catch(console.error);
    }
};

//Intersection Observer to observer intersection of spinner with viewport
const observer = new IntersectionObserver(loadOrders);
if (loadingSpinner) observer.observe(loadingSpinner);

/* ******************************
 * Changing text content of orders and products page links when device size in less than 480px
 ****************************** */
const productsPageLink = document.querySelector(".manage__products__link");
const ordersPageLink = document.querySelector(".new__order__link");

const mediaQuery = window.matchMedia("screen and (max-width:480px)");

mediaQuery.addListener(e => {
    if (e.matches) {
        productsPageLink.textContent = "Products";
        ordersPageLink.textContent = "Orders";
    } else {
        productsPageLink.textContent = "Manage Products";
        ordersPageLink.textContent = "Manage Orders";
    }
});

window.onload = e => {
    if (e.currentTarget.innerWidth <= 480) {
        productsPageLink.textContent = "Products";
        ordersPageLink.textContent = "Orders";
    }
};
