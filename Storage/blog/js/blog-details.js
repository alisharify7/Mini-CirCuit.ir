const owl_carousel_slider = $(".owl-carousel-blog-post-slider");
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
    nav: false,
    dots: false,

    responsive: {
        0: {
            items: 1,
        },
        250: {
            items: 1,
        },
        450: {
            items: 2,
        },
        650: {
            items: 3,
        },
        980: {
            items: 4,
        },
        1300: {
            items: 5,
        },
    },
});

function Copy2clipboard(text) {
    navigator.clipboard.writeText(text).then(function () {
        alert("متن با موفقیت کپی گردید")
    }, function (err) {
        alert("قابلیت کپی کردن متن در مرورگر شما پشتیبانی نمی شود")
    });
}