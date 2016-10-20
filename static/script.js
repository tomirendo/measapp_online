angular.module('MyApp', ['ngMaterial'])
.controller('AppCtrl', ['$scope', '$http', function($scope, $http, $mdSidenav){

  $scope.remove = function(array, index){
    array.splice(index,1);
  }


  $scope.devices = [];
  $scope.measurements = [];
  $scope.outputs = [];
  $scope.measurement_meta_data = {};
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
