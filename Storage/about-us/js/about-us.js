$(document).ready(function () {
    var awardSlider = $(".award-slider");
    awardSlider.owlCarousel({
        rtl: true,
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        autoplayTimeout: 2000,
        autoplayHoverPause: true,
        // lazyLoad: true,
        center: true,
        nav: false,
        dots: false,
        responsive: {
            0: {
                items: 1,
            },
            350: {
                items: 1,
            },
            450: {
                items: 2,
            },
            800: {
                items: 3,
            }
        }
    });
    var imageShowSlider = $(".gallery-slider-show");
    imageShowSlider.owlCarousel({
        rtl: true,
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        autoplayTimeout: 1000,
        autoplayHoverPause: true,
        // lazyLoad: true,
        center: true,
        nav: false,
        dots: false,
        responsive: {
            0: {
                items: 1,
            },
            350: {
                items: 1,
            },
            800: {
                items: 3,
            },
            900: {
                items: 4,
            },
            1100: {
                items: 5,
            },
            1300: {
                items: 6,
            }
        }
    });

    var factorySlider = $(".factory-slider");
    factorySlider.owlCarousel({
        rtl: true,
        loop: true,
        margin: 10,
        autoplay: true,
        responsiveClass: true,
        autoplayTimeout: 2000,
        autoplayHoverPause: true,
        // lazyLoad: true,
        center: true,
        nav: false,
        dots: false,
        responsive: {
            0: {
                items: 1,
            },
        }
    })
})
console.log("Lazy Load is off")