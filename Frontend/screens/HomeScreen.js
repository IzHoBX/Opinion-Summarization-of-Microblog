import * as WebBrowser from 'expo-web-browser';
import * as React from 'react';
import { Image, Platform, StyleSheet, Text, TextInput, TouchableOpacity, View, Dimensions, Container, Button } from 'react-native';
import { ScrollView } from 'react-native-gesture-handler';
import DropdownMenu from 'react-native';

import { MonoText } from '../components/StyledText';
import Posts from "../Posts.js"
import TabBarIcon from '../components/TabBarIcon';


export default function HomeScreen({ navigation }) {
  const [state, setState] = React.useState({posts:[]})
  const [positive, setPositive] = React.useState([])
  const [neutral, setNeutral] = React.useState([])
  const [negative, setNegative] = React.useState([])
  const [all, setAll] = React.useState([])

  React.useEffect(() => {
    function pullData() {
      var Httpreq = new XMLHttpRequest(); // a new request
      Httpreq.open("GET","http://localhost:7777/positive",false);
      Httpreq.send(null);
      var res = JSON.parse(Httpreq.responseText)["res"];
      setState({posts:res})
    }
    pullData()
  }, []);

  const [value, onChangeText] = React.useState('Useless Placeholder');

  return (
    <View style={styles.container} id="demo">
      <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
        <View style = {styles.sentimentContainer}>
          <TouchableOpacity style ={styles.positiveButton} onPress={()=> {
            console.log("positive")
            var Httpreq = new XMLHttpRequest(); // a new request
            Httpreq.open("GET","http://localhost:7777/positive",false);
            Httpreq.send(null);
            var res = JSON.parse(Httpreq.responseText)["res"];
            setState({posts:res})
            }}>
            <Image
            source={__DEV__
                ? require('../assets/images/happy.png')
                : require('../assets/images/happy.png')
            }
            style={styles.welcomeImage}
          />
          </TouchableOpacity>
          <TouchableOpacity style ={styles.neutralButton} onPress={()=>{
            console.log("neutral")
            var Httpreq = new XMLHttpRequest(); // a new request
            Httpreq.open("GET","http://localhost:7777/neutral",false);
            Httpreq.send(null);
            var res = JSON.parse(Httpreq.responseText)["res"];
            setState({posts:res})
            }}>
              <Image
            source={__DEV__
                ? require('../assets/images/face-to-face-icon-70.png')
                : require('../assets/images/face-to-face-icon-70.png')
            }
            style={styles.welcomeImage}
            />
          </TouchableOpacity>
          <TouchableOpacity style ={styles.negativeButton} onPress={()=> {
            console.log("negative")
            var Httpreq = new XMLHttpRequest(); // a new request
            Httpreq.open("GET","http://localhost:7777/negative",false);
            Httpreq.send(null);
            var res = JSON.parse(Httpreq.responseText)["res"];
            setState({posts:res})
            }}>
              <Image
            source={__DEV__
                ? require('../assets/images/sad-face.png')
                : require('../assets/images/sad-face.png')
            }
            style={styles.welcomeImage}
          />
          </TouchableOpacity>
        </View>
        <TouchableOpacity style ={styles.allButton} onPress={()=>{
            console.log("all")
            var Httpreq = new XMLHttpRequest(); // a new request
            Httpreq.open("GET","http://localhost:7777/all",false);
            Httpreq.send(null);
            var res = JSON.parse(Httpreq.responseText)["res"];
            setState({posts:res})
            }}>
            <Button title = "Show All" color="#003f5c"/>
          </TouchableOpacity>
        <View style={styles.getStartedContainer}>
          <Posts posts={state.posts}/>
        </View>
        </ScrollView>
    </View>
  );
}

const data = ["neutral", "positive", "negative"]

const styles = StyleSheet.create({
  sentimentContainer: {
    flex: 1,
    marginBottom: 15,
    justifyContent: 'center',
    flexDirection: 'row'
  },
  neutralButton: {
    marginLeft: 15
  },
  negativeButton: {
    marginLeft: 15
  },
  allButton: {
    flexDirection: 'row',
    justifyContent: 'center'
  },
  buttonText: {
    fontSize: 17,
    color: 'black',
    lineHeight: 24,
    textAlign: 'center',
  },
  container: {
    flex: 1,
    backgroundColor: '#F0F0F0',
  },
  developmentModeText: {
    marginBottom: 20,
    color: 'rgba(0,0,0,0.4)',
    fontSize: 14,
    lineHeight: 19,
    textAlign: 'center',
  },
  contentContainer: {
    paddingTop: 30,
  },
  welcomeContainer: {
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 20,
  },
  welcomeImage: {
    width: 100,
    height: 80,
    resizeMode: 'contain',
    marginTop: 3,
    marginLeft: -10,
  },
  getStartedContainer: {
    color: 'rgb(16,16,16)',
    alignItems: 'center',
  },
  getStartedText: {
    fontSize: 17,
    color: 'rgba(96,100,109, 1)',
    lineHeight: 24,
    textAlign: 'center',
  },
  helpLinkText: {
    fontSize: 14,
    color: '#2e78b7',
  },
  scrollContainer: {
    flex: 1,
  },
  box: {
    width: 150,
    height: 20,
    marginLeft: 15,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'grey',
  }
});
/*
<View style= {styles.scrollContainer}>
  <View style ={styles.box}><Text style={styles.getStartedText}> Box1</Text></View>
  <View style ={styles.box}><Text style={styles.getStartedText}> Box2</Text></View>
  <View style ={styles.box}><Text style={styles.getStartedText}> Box3</Text></View>
  <View style ={styles.box}><Text style={styles.getStartedText}> Box4</Text></View>
  <View style ={styles.box}><Text style={styles.getStartedText}> Box5</Text></View>
  <View style ={styles.box}><Text style={styles.getStartedText}> Box6</Text></View>
</View>*/
