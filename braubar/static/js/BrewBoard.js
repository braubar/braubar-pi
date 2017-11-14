$(document).ready(function () {
    $("#brew_form_submit").submit(function( event ) {

  // Stop form from submitting normally
  event.preventDefault();

  // Get some values from elements on the page:
  var $form = $( this ),
    term = $form.find( "input[name='brew_id_field']" ).val(),
    url = $form.attr( "action" );

  // Send the data using post
  var posting = $.post( url, { brew_id: term, test:12 } );

  // Put the results in a div
  posting.done(function( data ) {
    //var content = $( data ).find( "#content" );
    console.log(data)
    //$( "#result" ).empty().append( content );
  });
});

})

function startBrewing() {
    brew_id = $("brew_id_field").text
    $.post("brewboard/"+brew_id)
        .done(function( data ) {
                alert( "Data Loaded: " + data );
        });
}
