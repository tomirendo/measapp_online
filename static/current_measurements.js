angular.module('MyApp', ['ngMaterial'])
.controller('AppCtrl', ['$scope', '$http', '$mdDialog', function($scope, $http, $mdDialog, $mdSidenav){

  $scope.remove = function(array, index){
    array.splice(index,1);
  }
  $scope.open_window = function (url){
        window.open(url, "_blank");
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
  $scope.loading += 1;
  $scope.open = function(measurement_id){
    window.open("http://localhost:5000/static/measurement.html?measurement_id=" + measurement_id, "_blank");
  }
  $http.get("/all_measurements/").then(function(response){
      $scope.data= response.data;
      $scope.measurements = $scope.data.result;
      $scope.loading -= 1;
      //console.log($scope.devices);
  });

  }]).config(function($mdThemingProvider) {

    // Configure a dark theme with primary foreground yellow

    $mdThemingProvider.theme('docs-dark', 'default')
      .primaryPalette('blue-grey')
      .dark();

  });;
