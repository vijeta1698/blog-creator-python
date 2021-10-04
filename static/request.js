function getBlog(bid){
  $.ajax({
      type:"POST",
      url: '{{url_for('update')}}',
      data: { id : bid},
      success: function (result) {
          var Response = JSON.parse(result);
          alert(Response);
      }
  });