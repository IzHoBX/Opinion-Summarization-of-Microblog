import React, { Component } from 'react'
import { View, Text, TouchableOpacity, TextInput, StyleSheet } from 'react-native'

export default function AddScreen({ navigation }) {
  const [title, setTitle] = React.useState({title:""})
  const [text, setText] = React.useState({text:""})

  return (
     <View style = {styles.container}>

        <TextInput style = {styles.input}
           underlineColorAndroid = "transparent"
           placeholder = "What's on your mind?"
           placeholderTextColor = "#696969"
           maxLength={150}
           autoCapitalize = "none"
           onChangeText = {(newText)=>setText({text:newText})}/>

        <TouchableOpacity
           style = {styles.publishButton}
           onPress={()=> {
             console.log("sending" + text)
             var Httpreq = new XMLHttpRequest(); // a new request
             Httpreq.open("GET","http://localhost:7777/SUBMIT?" + text.text,false);
             Httpreq.send(null);
             var res = JSON.parse(Httpreq.responseText)["res"];
             alert(res)
           }}>
           <Text style = {styles.publishButtonText}> Publish </Text>
        </TouchableOpacity>
     </View>
  )
}

const styles = StyleSheet.create({
   container: {
      paddingTop: 23
   },
   input: {
      margin: 15,
      height: 40,
      borderColor: '#003f5c',
      borderWidth: 1
   },
   publishButton: {
      backgroundColor: '#003f5c',
      padding: 10,
      margin: 15,
      height: 40,
   },
   publishButtonText:{
      color: 'white'
   }
})

/*
<TextInput style = {styles.input}
   underlineColorAndroid = "transparent"
   placeholder = "Title"
   placeholderTextColor = "#696969"
   maxLength={30}
   autoCapitalize = "none"
   onChangeText = {(newText)=>setTitle({title:newText})}/>*/
