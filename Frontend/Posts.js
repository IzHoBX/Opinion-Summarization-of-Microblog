import React from 'react'
import {Dimensions, StyleSheet, View, Container, ListView} from 'react-native'

const x = {
  fontSize: 10,
  color: 'rgb(256, 256, 256)',
  lineHeight: 24,
  textAlign: 'center',
  'font-family': 'verdana',
  flexWrap: 'wrap',
  flex: 1,
  width: 500,
  'word-wrap': "break-word",
  "overflow-wrap": "break-word"
}

const Posts = ({ posts }) => {
  /*return (
    <View>
      {posts.map((post) => (
        <View style ={styles.box} onclick={()=>alert({post})}><h1 style={x}>{post}</h1></View>
      ))}
    </View>
  )*/
  console.log(posts)
  const ds = new ListView.DataSource({rowHasChanged: (r1, r2) => r1 !== r2});
  var x = ds.cloneWithRows(posts)
  return (
    <ListView
      style = {{
        marginHorizontal: 50,
        borderLeftWidth :1,
        borderLeftColor: '#000',
        borderTopWidth :1,
        borderTopColor: '#000',
        borderRightWidth :1,
        borderRightColor: '#000',
      }}
      dataSource={x}
      renderRow={
          (rowData) =>
              <h1 style={{fontSize: 20, 'font-family': 'verdana'}}>{rowData}</h1>}
      renderSeparator={(sectionId, rowId) =>
                        <View key={rowId} style={styles.separator} />}
    />
  )
};

const styles = StyleSheet.create({
  scrollContainer: {
    flex: 1,
  },
  getStartedText: {
    fontSize: 17,
    color: 'rgba(96,100,109, 1)',
    lineHeight: 24,
    textAlign: 'center',
  },
  separator: {
       height: 0.5, width: "100%", backgroundColor: "#000"
   },
  box: {
    margin: 2,
    width: Dimensions.get('window').width / 2 -6,
    height: 150,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#003f5c',
    flexShrink: 1,
  }
});

export default Posts
