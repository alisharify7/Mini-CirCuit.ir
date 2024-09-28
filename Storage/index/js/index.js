window.addEventListener("resize", e => {
    // close mobile size category modal
    if (window.innerWidth >= 765) {
        $("#category-modal > div > div > div.modal-header > button").click()
    }
})


$(document).ready(function () { //index first slider banner
    const owl_carousel_slider = $(".owl-carousel-slider");
    owl_carousel_slider.owlCarousel({
        rtl: true,
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        autoplayTimeout: 2000,
        autoplayHoverPause: true,
        lazyContent: true,
        lazyLoad: true,
        center: true,
        nav: true,

        responsive: {
            0: {
                items: 1,
            },
        },
    });

    const blog_news_owl = $(".blog-news-slider");
    blog_news_owl.owlCarousel({
        rtl: true,
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        autoplayTimeout: 2000,
        autoplayHoverPause: true,
        lazyContent: true,
        lazyLoad: true,
        center: true,
        nav: true,
        dots: true,
        responsive: {
            0: {
                items: 1,
            },
            250: {
                items: 1,
            },
            650: {
                items: 2,
            },
            980: {
                items: 3,
            },
            1300: {
                items: 3,
            },
        },

    });



    const buy_aboard_slider = $(".buy-from-every-where");
    buy_aboard_slider.owlCarousel({
        rtl: true,
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        autoplayTimeout: 1500,
        autoplayHoverPause: true,
        lazyContent: true,
        lazyLoad: true,
        center: true,
        nav: false,
        dots: false,
        pagination: false,
        navigation: true,
        responsive: {
            0: {
                items: 1,
            }
        },
        navText: ["<i class='bi bi-chevron-right display-4 fw-bold mt-3 '></i>", "<i class='bi bi-chevron-left display-4 fw-bold mt-3 '></i>"]

    });


});
