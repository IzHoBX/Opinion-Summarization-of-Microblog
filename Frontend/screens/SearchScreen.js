import React from 'react';
import { Image, TextInput, StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import { SearchBar } from 'react-native-elements';


export default function SearchScreen({navigation}) {
  const [state, setState] = React.useState({state:""})

  return  (
    <View style={styles.container}>
    <SearchBar
      placeholder="Type Here..."
      onChangeText={(newText)=>setState({state:newText})}
      value="Search"
    />
    <TouchableOpacity style ={styles.box} onPress={()=>{
      var Httpreq = new XMLHttpRequest(); // a new request
      Httpreq.open("GET","http://localhost:7777/SET?spacex",false);
      Httpreq.send(null);
      navigation.navigate("Home")
    }}><Text style={styles.getStartedText}> SpaceX</Text></TouchableOpacity>
    <TouchableOpacity style ={styles.box} onPress={()=>{
      var Httpreq = new XMLHttpRequest(); // a new request
      Httpreq.open("GET","http://localhost:7777/SET?brexit",false);
      Httpreq.send(null);
      navigation.navigate("Home")
    }}><Text style={styles.getStartedText}> Brexit</Text></TouchableOpacity>
    <TouchableOpacity style ={styles.box} onPress={()=>{
      var Httpreq = new XMLHttpRequest(); // a new request
      Httpreq.open("GET","http://localhost:7777/SET?nobel",false);
      Httpreq.send(null);
      navigation.navigate("Home")
    }}><Text style={styles.getStartedText}> Nobel Prize</Text></TouchableOpacity>
    <TouchableOpacity style ={styles.box} onPress={()=>{
      var Httpreq = new XMLHttpRequest(); // a new request
      Httpreq.open("GET","http://localhost:7777/SET?note7",false);
      Httpreq.send(null);
      navigation.navigate("Home")
    }}><Text style={styles.getStartedText}> Note 7</Text></TouchableOpacity>
    <TouchableOpacity style ={styles.box} onPress={()=>{
      var Httpreq = new XMLHttpRequest(); // a new request
      Httpreq.open("GET","http://localhost:7777/SET?isis",false);
      Httpreq.send(null);
      navigation.navigate("Home")
    }}><Text style={styles.getStartedText}> ISIS</Text></TouchableOpacity>
    </View>
  )

}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
    alignItems: 'center',
    justifyContent: 'flex-start',
  },
  box: {
    width: 150,
    height: 60,
    marginTop: 30,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgb(27,149,224)',
  },
  getStartedText: {
    fontSize: 17,
    color: 'black',
    lineHeight: 24,
    textAlign: 'center',
  },
});
