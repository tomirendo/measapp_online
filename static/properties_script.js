angular.module('MyApp', ['ngMaterial'])
.controller('AppCtrl', ['$scope', '$http', '$mdDialog', function($scope, $http, $mdDialog, $mdSidenav){

  $scope.remove = function(array, index){
    array.splice(index,1);
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
  $scope.log = function(){
    console.log($scope.measurements);
  }
  $scope.add_measurement = function(){
    $scope.measurements.push({device : '', input : ''});
    console.log($scope.measurements);
  };
  $scope.add_output = function(){
    $scope.outputs.push({device : '', output : ''});
  }
  $scope.select_device = function(device){
    $scope.selected_device = device;
    $scope.outputs_value = [];
    for (output in $scope.selected_device.outputs){
       $scope.outputs_value.push ({name :$scope.selected_device.outputs[output],value : null});
    }
    console.log($scope.outputs_value);
  }
  $scope.update = function(device){
    $scope.loading += 1;
    $http.post('/update_property/', device ).then(function(result){
      $scope.loading -= 1;
      data = result.data;
      if (data.error){
        $scope.show_alert(data.error_description);
    } else {

    }
    }, function (error){
      $scope.loading = false;
       $scope.show_alert(error);
    });

  }
  $scope.is_number_property = function(property){
    return property.type == 'number';
  }
  $scope.update_outputs = function(selected_device){
    console.log($scope.outputs_value);
    for (output in $scope.outputs_value){
      output = $scope.outputs_value[output];
      if (!(output.value === null)){
        $scope.loading+=1; 
        $http.post('/update_output/', 
            {name : $scope.selected_device.name,
              output : output.name,
              value : output.value})
        .then(function (result){
          $scope.loading -= 1;
          data = result.data;
          if (data.error){
            $scope.show_alert(data.error_description);
          }
        }, function (error){
          $scope.loading -= 1 ;
        });
      }
    }
  }
  $http.get("/devices/").then(function(response){
      $scope.devices = response.data;
      console.log($scope.devices);
  });
  }]).config(function($mdThemingProvider) {

    // Configure a dark theme with primary foreground yellow

    $mdThemingProvider.theme('docs-dark', 'default')
      .primaryPalette('blue-grey')
      .dark();

  });;
