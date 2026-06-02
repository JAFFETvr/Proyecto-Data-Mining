import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { StatusBar } from 'expo-status-bar';

export default function Layout() {
  return (
    <>
      <StatusBar style="light" />
      <Tabs
        screenOptions={{
          tabBarStyle: {
            backgroundColor: '#0b2f1e',
            borderTopColor: '#1b5e20',
            borderTopWidth: 1,
          },
          tabBarActiveTintColor: '#fdd835',
          tabBarInactiveTintColor: '#b7d6c2',
          headerStyle: { backgroundColor: '#0b2f1e' },
          headerTintColor: '#e9f5e9',
          headerTitleStyle: { fontWeight: '700' },
        }}
      >
        <Tabs.Screen
          name="index"
          options={{
            title: 'Dashboard',
            tabBarIcon: ({ color, size }) => (
              <Ionicons name="bar-chart" size={size} color={color} />
            ),
          }}
        />
        <Tabs.Screen
          name="predict"
          options={{
            title: 'Predicción',
            tabBarIcon: ({ color, size }) => (
              <Ionicons name="analytics" size={size} color={color} />
            ),
          }}
        />
      </Tabs>
    </>
  );
}
