import React, { useState, useEffect } from 'react';
import { SafeAreaView, View, Text, TextInput, Button, ScrollView, StyleSheet, ActivityIndicator } from 'react-native';
{/* OBS: importações de api.ts devem ser relativas ao contexto do projeto React Native */}
import { searchAPI } from './api';

interface DocsSearchScreenProps {
  navigation: any;
}

const DocsSearchScreen: React.FC<DocsSearchScreenProps> = ({ navigation }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  const performSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setResults([]);

    try {
      const results = await searchAPI(query);
      setResults(results);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const goBackToChat = () => {
    navigation.navigate('Chat');
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Buscar Documentação</Text>
        <Button title="Voltar" onPress={goBackToChat} style={styles.backButton} />
      </View>

      <View style={styles.searchContainer}>
        <TextInput
          placeholder="Digite sua busca..."
          value={query}
          onChangeText={setQuery}
          style={styles.input}
          placeholderTextColor="#aaa"
        />
        <Button title="Buscar" onPress={performSearch} style={styles.searchButton} />
      </View>

      {loading && (
        <View style={styles.loading}>
          <ActivityIndicator size="large" />
        </View>
      )}

      {results.length > 0 && (
        <View style={styles.resultsContainer}>
          <Text style={resultsTitle}>Resultados ({results.length})</Text>
          <ScrollView
            contentContainerStyle={styles.resultsList}
            showsVerticalScrollIndicator={false}
          >
            {results.map((result, index) => (
              <View key={index} style={styles.resultItem}>
                <Text style={styles.resultTitle}>{result.file}</Text>
                <Text style={styles.resultExcerpt}>{result.excerpt}</Text>
              </View>
            ))}
          </ScrollView>
        </View>
      )}

      {results.length === 0 && query.trim().length > 0 && (
        <View style={styles.noResults}>
          <Text>Nenhum resultado encontrado</Text>
        </View>
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#0066cc',
    padding: 16,
    paddingTop: 24,
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    borderBottomWidth: 1,
    borderColor: '#ccc',
  },
  searchContainer: {
    margin: 16,
    padding: 12,
    backgroundColor: '#fafafa',
    borderRadius: 8,
  },
  input: {
    flex: 1,
    height: 48,
    paddingHorizontal: 12,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 20,
    fontSize: 14,
    backgroundColor: '#fff',
  },
  searchButton: {
    marginLeft: 10,
    backgroundColor: '#0066cc',
    paddingHorizontal: 15,
    paddingVertical: 8,
  },
  resultsContainer: {
    marginTop: 20,
    paddingHorizontal: 16,
  },
  resultsTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  resultsList: {
    marginTop: 10,
  },
  resultItem: {
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    backgroundColor: '#fff',
  },
  resultTitle: {
    fontWeight: 'bold',
    fontSize: 14,
    color: '#0066cc',
  },
  resultExcerpt: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  noResults: {
    color: '#888',
    fontSize: 14,
    marginTop: 20,
    textAlign: 'center',
  },
  backButton: {
    margin: 16,
  },
});

export default DocsSearchScreen;