var app = angular.module('imgSearch', ['ngFileUpload']);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('//');
  $interpolateProvider.endSymbol('//');
}]);

// hide initial
$("#searching").hide();
$("#query").hide();
$("#results").hide();
$("#error").hide();

app.controller('SearchCtrl', ['$scope', 'Upload', function SearchController($scope, Upload){
  $scope.data = {};
	$scope.name = "aria";
	console.log($scope.name);
	$scope.linker = "static/imgDB/"

  $scope.urlMapper = function(dict){
    var prefix = window.location.href + $scope.linker;
    var uploadPrefix = "static/upload/";
    $scope.queryImg = uploadPrefix + $scope.file.name;

    return dict.map(function(obj){
      var rObj = {};
      rObj["url"] = prefix + obj.image;
      rObj["score"] = obj.score;
      rObj["name"] = obj.image.split(".")[0];
      return rObj;
    });
  };

  // upload later on form submit or something similar
  $scope.submit = function() {
      $scope.upload($scope.file);
      // if ($scope.form.file.$valid && $scope.file && !$scope.file.$error) {
      //   $scope.upload($scope.file);
      // }
  };

  // upload on file select or drop
    $scope.upload = function (file) {
      $("#searching").show();

        Upload.upload({
            url: '/search',
            fields: {'username': $scope.username},
            file: file
        }).progress(function (evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
        }).success(function (data, status, headers, config) {
            $("#searching").hide();

            console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
            // console.log(JSON.stringify(data));
            $scope.searchResults = $scope.urlMapper(data["results"]);
            console.log($scope.searchResults);
            $("#query").show();
            $("#results").show();
        }).error(function (data, status, headers, config) {
            console.log('error status: ' + status);
        });
    };
}]);
