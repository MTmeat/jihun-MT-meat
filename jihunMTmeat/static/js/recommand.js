function meatRecommand() {
    var manNum = parseInt($("#man").val());
    var womanNum = parseInt($("#woman").val());


    if (manNum + womanNum > 20) {
        manNum = manNum * 1.2;
        womanNum = womanNum * 0.8;
    }

    var 고기근수 = Math.round((manNum + womanNum) * 0.5);

    var 삼겹근수 = Math.round(고기근수 * 0.5);
    var 목살근수 = 삼겹근수;

    if (고기근수 % 2 != 0) {
        목살근수 = 삼겹근수 - 1;
    }

    $("#추천삼겹").text(삼겹근수);
    $("#추천목살").text(목살근수);

}


function calculateTotalPrice() {
    var 삼겹가격 = $("#삼겹").attr('price');
    var 목살가격 = $("#목살").attr('price');

    var 삼겹개수 = $("#삼겹").val();
    var 목살개수 = $("#목살").val();

    var totalPrice = 삼겹가격 * 삼겹개수 + 목살가격 * 목살개수;

    $("#total").text(totalPrice+'원');
}

