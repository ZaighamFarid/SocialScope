//
//  SocialScopeApp.swift
//  SocialScope
//
//  Main entry point of the app
//

import SwiftUI
import Combine

@main
struct SocialScopeApp: App {
    // App-wide settings that persist across screens
    @StateObject private var settings = AppSettings()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(settings)
        }
    }
}

// Settings that are available throughout the app
class AppSettings: ObservableObject {
    @Published var offlineMode: Bool = false
}
