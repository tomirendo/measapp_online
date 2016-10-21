angular.module('MyApp', ['ngMaterial'])
.controller('AppCtrl', ['$scope', '$http', '$mdDialog', function($scope, $http, $mdDialog, $mdSidenav){

  $scope.remove = function(array, index){
    array.splice(index,1);
  }

  $scope.devices = [];
  $scope.selected_device = {};
  $scope.loading = false;
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
  }
  $scope.update = function(device){
    $scope.loading = true;
    $http.post('/update_property/', device ).then(function(result){
      $scope.loading = false;
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
