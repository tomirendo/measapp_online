angular.module('MyApp', ['chart.js','ngMaterial'])
.controller('AppCtrl', ['$scope', '$http', '$mdDialog', function($scope, $http, $mdDialog, $mdSidenav){

  $scope.remove = function(array, index){
    array.splice(index,1);
  }
  $scope.zip = function zip(arrays) {
    return arrays[0].map(function(_,i){
        return arrays.map(function(array){return array[i]})
    });
}
  $scope.int_to_bool = function(n){
    if (n == 0){
      return false;
    } else {
      return true;
    }
  }
  $scope.bool_to_int = function(b){
    if (b){
      return 1;
    } else {
      return 0;
    }
  }
  $scope.open_window = function (url){
        window.open(url, "_blank");
  }

  $scope.devices = [];
  $scope.loading = 0;
  $scope.outputs_value = [];

  $scope.show_alert = function(text){
      $mdDialog.show(
        $mdDialog.alert()
        .title('An Error Occurred')
        .textContent(text)
        .ok("Got it!").clickOutsideToClose(true));
  }
  var patt = new RegExp("measurement_id=(\\d+)");
  $scope.measurement_id = patt.exec(document.location.href)[1];



  $scope.reload_data = function (){
  $http.get("/measurement/"+$scope.measurement_id+"/").then(function(response){
    if (response.data.error){
      $scope.show_alert(response.data.error_description);
    } else{
      $scope.measurement_data = response.data.result ;
      console.log($scope.measurement_data);
      if ($scope.first_time){
      $scope.series = $scope.measurement_data.outputs.map( 
                                                  function(output) { return output.device + ":" + output.output});
      $scope.series = $scope.series.concat($scope.measurement_data.inputs.map( 
                                                  function(input) { return input.device + ":" + input.input}));
      $scope.labels = $scope.measurement_data.range;
      $scope.first_time = false;
      $scope.new_input_name = $scope.series[0];
    }
      $scope.data = $scope.zip($scope.measurement_data.results.map(function(res) { return res.slice(1);}));
      if ($scope.measurement_data.running){
        setTimeout($scope.reload_data, 2);
      } 
      $scope.date = new Date().getTime();
    }
    
  });};
  $scope.stop_measurement = function(){
    console.log("Stop Measurement");
    $http.get("/stop_measurement/"+$scope.measurement_id+"/").then(function (response){
      if (response.data.error){
        $scope.show_alert(response.data.error_description);
      } else {

      }
    }, function (error){
      $scope.show_alert(error);
    });
  }



  $scope.first_time = true;
  setTimeout($scope.reload_data, 3);

  $scope.data = [];
  $scope.series=[];
  $scope.options = {};
  $scope.graphs = [] ;
  $scope.x_axis = "";
  $scope.y_axis = "";
  $scope.date = new Date().getTime();

  $scope.add_graph = function() {
    index_of_x_axis = $scope.series.indexOf($scope.x_axis);
    index_of_y_axis = $scope.series.indexOf($scope.y_axis);
    $scope.graphs.push({graph_x_axis: index_of_x_axis, graph_y_axis: index_of_y_axis, input_name : $scope.new_input_name, diff : false})
  }

  }]).config(function($mdThemingProvider) {

    // Configure a dark theme with primary foreground yellow

    $mdThemingProvider.theme('docs-dark', 'default')
      .primaryPalette('blue-grey')
      .dark();

  });