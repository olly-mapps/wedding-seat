$(document).ready(function(){
  $("h1").css("color", "#0088ff");

  var group_count = 1;
  var row_count = 0;

  var name_count = 0;

  $("#add-group").click(function(){
    group_count += 1;
    $("#row" + row_count).append("<td> \
                                  <div id = 'name-input-" + (group_count) + "' class = 'name-input'> \
                                  <input type = 'text' id = 'group-" + group_count + "-name'> \
                                  <button type = 'button' class = 'guest-name' id='guest-name-" + (group_count) +"'>Set Group Name</button> \
                                  </div> \
                                  <div class = 'group-type'> \
                                  <form id = 'group-" + (group_count) + "-type-name'> \
                                  <select> \
                                  <option>Family</option> \
                                  <option>Friends</option> \
                                  <option>Couple</option> \
                                  <option>Other</option> \
                                  </select> \
                                  </form> \
                                  </div> \
                                  <div id = 'group-input-" + (group_count) +"' class = 'group-input'> \
                                  <ol class = 'group-list' id= 'group-" + (group_count) + "'></ol> \
                                  <input type='text' name='new-guest' id = 'new-guest-" + (group_count) + "'> \
                                  <button type='button' class = 'add-guest' id='add-guest-" + (group_count) + "'>Add Guest</button> \
                                  </div> \
                                  </td>");
    
    if (group_count%3 == 0) {
      row_count+=1
      $("#group-list-table").append("<tr id = 'row" + row_count + "'></tr>")
    }
  });

  $(document).on('click', '.add-guest', function(){
    var group_id = this.id;
    group_number = group_id.match(/(\d+)/)[0];
    new_guest = $("#new-guest-" + group_number).val();
    $("#group-" + group_number).append("<li>" + new_guest + "</li>");
  });

  $(document).on('click', '.guest-name', function(){
    var group_id = this.id;
    group_number = group_id.match(/(\d+)/)[0];
    $("#group-input-" + group_number).toggle();
    group_name = $("#group-" + group_number + "-name").val();
    $("#name-input-" + group_number).html("<div class = 'name-type'> \
                                          <label><strong> " + group_name + " </strong></label> \
                                          </div> ");
  });

  $(document).on('click', '.add-person', function(){
    name_count+=1;
    $("#individual-list-div").show();
    $("#individual-list").append("<tr><td> <input class = 'individual-name' id = 'individual-name-" + name_count + "' placeholder='Please Input Name'> \
                                  <button id = 'set-individual-name-" + name_count + "'>Set Name</button></td></tr>");
  });

});