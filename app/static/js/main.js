$(document).ready(function() {
    $.ajax({
      url: '/api/warung',
    })
    .done(function(res) {
      var warungList=$('#warung-list');
      for (var i = 0; i < res.data.length; i++) {
        var card=`<div class="col-md-3 col-sm-12 mb-3">
              <div class="card">
                <img class="card-img-top" src="/static/kantin1.jpeg">
                <div class="card-body">
                  <h4 class="card-title">`+res.data[i].nama+`</h4>
                  <p class="card-text">&#x2605; `+res.data[i].rating+`</p>
                  <button class="btn btn-primary warung-detail-btn" onclick="getWarungDetail(`+res.data[i].id+`)" data-toggle="modal" data-target="#warungDetail" type="button">Details</button>
                </div>
              </div>
            </div>`;
        warungList.append(card);
      }
    });

});

function getWarungDetail(id) {
  $.ajax({
    url: '/api/warung/'+id,
  })
  .done(function(res) {

    var warung=res.data.warung;
    var menus=res.data.menu;
    var pedagang=res.data.pedagang;

    $('#nama-warung').html(warung.nama);
    $('#rating-warung').html(warung.rating);

    //get and show nama-nama pedagang
    var pedagang2=""
    for (var i = 0; i < pedagang.length; i++) {
      pedagang2+=pedagang[i].nama+", ";
    }
    $('#pedagang-warung').html(pedagang2);

    //get makanan and minuman list
    var makanan="",minuman="";
    for (var i = 0; i < menus.length; i++) {
      var menu=`<li class="menu-item d-flex flex-row justify-content-start mb-3">
        <img src="/static/bakso.jpeg" class="menu-img">
        <div class="ml-3">
          <h5>`+menus[i].nama+`</h5>
          <small>Rp. `+menus[i].harga+`,-</small>
        </div>
      </li>`;

      if (menus[i].tipe=="Makanan") {
        makanan+=menu;
      }
      else {
        minuman+=menu;
      }
    }
    //show makanan dan minuman in the list
    $('#menu-makanan').html(makanan);
    $('#menu-minuman').html(minuman);

  
  });
}
