angular.module('MyApp', ['ngMaterial'])
.controller('AppCtrl', ['$scope', '$http', '$mdDialog', function($scope, $http, $mdDialog, $mdSidenav){

  $scope.remove = function(array, index){
    array.splice(index,1);
  }

  $scope.show_alert = function(text){
      $mdDialog.show(
        $mdDialog.alert()
        .title('An Error Occurred')
        .textContent(text)
        .ok("Got it!").clickOutsideToClose(true));
  }
  $scope.devices = [];
  $scope.measurements = [];
  $scope.outputs = [];
  $scope.loading = 0;
  $scope.measurement_meta_data = {};
  $scope.log = function(){
    console.log($scope.measurements);
  }
  $scope.add_measurement = function(){
    $scope.measurements.push({device : '', input : ''});
    console.log($scope.measurements);
  };
  $scope.add_output = function(){
    $scope.outputs.push({device : '', output : '', begin_value : null, end_value : null, steps : null});
  }
  $scope.init_device = function(device, output, value){
    $scope.loading += 1;
    $http.post('/update_output/', {name : device.name, 
                                   output : output, 
                                value : value })
    .then(function (result){
      $scope.loading -=1;
      if (result.data.error){
        $scope.show_alert(result.data.error_description);
      } else{
        ;
      }

    }, function(error){
      $scope.loading -= 1;
      $scope.show_alert("Connection Error, STATUS : " + error.status);
    });

  }
  $scope.begin_measurement = function(){
    $scope.loading += 1;
    $scope.outputs.forEach(function (output){ console.log(output); output.name = $scope.devices[output.device_id].name;});
    $scope.measurements.forEach(function (input ){ console.log(input); input.name = $scope.devices[input.device_id].name;});
    $http.post('/begin_measurement/', {name: $scope.measurement_meta_data.name, step_time : $scope.measurement_meta_data.step_time,
                          outputs : $scope.outputs, measurements : $scope.measurements})
    .then(function(result){
      $scope.loading-=1;
      if (result.data.error){
        $scope.show_alert(result.data.error_description);
      } else {
        window.open("http://localhost:5000/static/measurement.html?measurement_id=" + result.data.result.measurement_id, "_blank");
      }

    }, function(error){
      $scope.loading -=1;
      $scope.show_alert("Connection Error, Status : " + error.status);

    });
  }
  $scope.loading += 1;
  $http.get("/devices/").then(function(response){
      $scope.devices = response.data;
      $scope.loading -= 1;
      console.log($scope.devices);
  });

  }]).config(function($mdThemingProvider) {

    // Configure a dark theme with primary foreground yellow

    $mdThemingProvider.theme('docs-dark', 'default')
      .primaryPalette('blue-grey')
      .dark();

  });;
