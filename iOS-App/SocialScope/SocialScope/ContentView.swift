//
//  ContentView.swift
//  SocialScope
//
//  Main UI of the app - all the beautiful screens and components
//

import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = AnalyzerViewModel()
    @EnvironmentObject var settings: AppSettings
    
    var body: some View {
        ZStack {
            // Beautiful gradient background
            LinearGradient(
                colors: [
                    Color(red: 0.4, green: 0.2, blue: 0.8),
                    Color(red: 0.2, green: 0.1, blue: 0.5)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            ScrollView {
                VStack(spacing: 24) {
                    // Header with app title and offline toggle
                    headerView
                    
                    // URL input field
                    urlInputSection
                    
                    // Show results when we have them
                    if let result = viewModel.analysisResult {
                        resultsView(result: result)
                    }
                }
                .padding()
            }
        }
        .alert("Error", isPresented: $viewModel.showError) {
            Button("OK", role: .cancel) { }
        } message: {
            Text(viewModel.errorMessage ?? "Something went wrong")
        }
        .onChange(of: settings.offlineMode) { newValue in
            viewModel.toggleOfflineMode(newValue)
        }
    }
    
    // MARK: - Header
    
    private var headerView: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text("Social Scope")
                    .font(.system(size: 32, weight: .bold, design: .rounded))
                    .foregroundColor(.white)
                
                Text("AI-Powered Social Analysis")
                    .font(.subheadline)
                    .foregroundColor(.white.opacity(0.8))
            }
            
            Spacer()
            
            // Toggle for offline demo mode
            Button(action: {
                settings.offlineMode.toggle()
                UIImpactFeedbackGenerator(style: .light).impactOccurred()
            }) {
                Image(systemName: settings.offlineMode ? "wifi.slash" : "wifi")
                    .font(.title2)
                    .foregroundColor(.white)
                    .frame(width: 50, height: 50)
                    .background(Color.white.opacity(0.2))
                    .clipShape(Circle())
            }
        }
        .padding(.top, 20)
    }
    
    // MARK: - URL Input
    
    private var urlInputSection: some View {
        VStack(spacing: 16) {
            TextField("Enter social media URL", text: $viewModel.urlInput)
                .textFieldStyle(GlassTextFieldStyle())
                .textInputAutocapitalization(.never)
                .autocorrectionDisabled()
            
            Button(action: {
                Task {
                    await viewModel.analyzeURL()
                }
            }) {
                HStack {
                    if viewModel.isLoading {
                        ProgressView()
                            .tint(.white)
                    } else {
                        Image(systemName: "sparkles")
                        Text("Analyze")
                            .fontWeight(.semibold)
                    }
                }
                .frame(maxWidth: .infinity)
                .frame(height: 56)
                .background(
                    LinearGradient(
                        colors: [Color.purple, Color.blue],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .foregroundColor(.white)
                .clipShape(RoundedRectangle(cornerRadius: 16))
            }
            .disabled(viewModel.isLoading)
            
            if settings.offlineMode {
                Label("Demo Mode Active", systemImage: "info.circle.fill")
                    .font(.caption)
                    .foregroundColor(.yellow)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(Color.yellow.opacity(0.2))
                    .clipShape(Capsule())
            }
        }
    }
    
    // MARK: - Results
    
    private func resultsView(result: AnalysisResponse) -> some View {
        VStack(spacing: 20) {
            // Summary card
            SummaryCardView(
                platform: result.platform,
                summary: result.summary,
                sentiment: result.sentiment
            )
            
            // Key topics
            topicsView(topics: result.keyTopics)
            
            // Suggested comments with tone selection
            commentsView(comments: result.suggestedComments)
            
            // Reset button
            Button(action: {
                withAnimation {
                    viewModel.reset()
                }
            }) {
                Label("New Analysis", systemImage: "arrow.clockwise")
                    .font(.headline)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .frame(height: 50)
                    .background(Color.white.opacity(0.2))
                    .clipShape(RoundedRectangle(cornerRadius: 12))
            }
        }
        .transition(.scale.combined(with: .opacity))
    }
    
    // Key topics section
    private func topicsView(topics: [String]) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Key Topics")
                .font(.headline)
                .foregroundColor(.white)
            
            FlowLayout(spacing: 8) {
                ForEach(topics, id: \.self) { topic in
                    TopicChip(text: topic)
                }
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(20)
        .background(Color.white.opacity(0.15))
        .clipShape(RoundedRectangle(cornerRadius: 20))
    }
    
    // Comments section with tone selector
    private func commentsView(comments: SuggestedComments) -> some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Suggested Comments")
                .font(.headline)
                .foregroundColor(.white)
            
            // Tone selection buttons
            HStack(spacing: 12) {
                ForEach(CommentTone.allCases, id: \.self) { tone in
                    ToneButton(
                        tone: tone,
                        isSelected: viewModel.selectedTone == tone,
                        action: {
                            withAnimation(.spring(response: 0.3)) {
                                viewModel.selectedTone = tone
                            }
                            UIImpactFeedbackGenerator(style: .light).impactOccurred()
                        }
                    )
                }
            }
            
            // The actual comment
            SuggestedCommentView(
                comment: viewModel.currentComment,
                onCopy: {
                    viewModel.copyComment(viewModel.currentComment)
                }
            )
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(20)
        .background(Color.white.opacity(0.15))
        .clipShape(RoundedRectangle(cornerRadius: 20))
    }
}

// MARK: - Custom Components

// Glass-style summary card
struct SummaryCardView: View {
    let platform: String
    let summary: String
    let sentiment: Sentiment
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: platformIcon(platform))
                    .foregroundColor(.white)
                Text(platform)
                    .font(.headline)
                    .foregroundColor(.white)
                
                Spacer()
                
                SentimentTagView(sentiment: sentiment)
            }
            
            Text(summary)
                .font(.body)
                .foregroundColor(.white.opacity(0.9))
                .lineSpacing(4)
        }
        .padding(20)
        .background(Color.white.opacity(0.15))
        .clipShape(RoundedRectangle(cornerRadius: 20))
    }
    
    private func platformIcon(_ platform: String) -> String {
        switch platform.lowercased() {
        case "twitter", "x":
            return "number.circle.fill"
        case "reddit":
            return "message.circle.fill"
        case "medium":
            return "doc.text.fill"
        default:
            return "link.circle.fill"
        }
    }
}

// Sentiment badge
struct SentimentTagView: View {
    let sentiment: Sentiment
    
    var body: some View {
        HStack(spacing: 4) {
            Image(systemName: sentimentIcon)
                .font(.caption)
            Text(sentiment.overall)
                .font(.caption)
                .fontWeight(.semibold)
            Text("(\(Int(sentiment.confidence * 100))%)")
                .font(.caption2)
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 6)
        .background(sentimentColor.opacity(0.3))
        .foregroundColor(.white)
        .clipShape(Capsule())
    }
    
    private var sentimentIcon: String {
        switch sentiment.overall.lowercased() {
        case "positive":
            return "hand.thumbsup.fill"
        case "negative":
            return "hand.thumbsdown.fill"
        default:
            return "minus.circle.fill"
        }
    }
    
    private var sentimentColor: Color {
        switch sentiment.overall.lowercased() {
        case "positive":
            return .green
        case "negative":
            return .red
        default:
            return .yellow
        }
    }
}

// Topic chip/bubble
struct TopicChip: View {
    let text: String
    
    var body: some View {
        Text(text)
            .font(.subheadline)
            .padding(.horizontal, 16)
            .padding(.vertical, 8)
            .background(Color.white.opacity(0.25))
            .foregroundColor(.white)
            .clipShape(Capsule())
    }
}

// Tone selection button
struct ToneButton: View {
    let tone: CommentTone
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 4) {
                Text(tone.emoji)
                    .font(.title3)
                Text(tone.rawValue)
                    .font(.caption2)
                    .fontWeight(isSelected ? .bold : .regular)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 12)
            .background(
                isSelected
                    ? Color.white.opacity(0.3)
                    : Color.white.opacity(0.1)
            )
            .foregroundColor(.white)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.white.opacity(isSelected ? 0.5 : 0), lineWidth: 2)
            )
        }
    }
}

// Comment display with copy button
struct SuggestedCommentView: View {
    let comment: String
    let onCopy: () -> Void
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(comment)
                .font(.body)
                .foregroundColor(.white.opacity(0.9))
                .lineSpacing(4)
            
            Button(action: onCopy) {
                HStack {
                    Image(systemName: "doc.on.doc.fill")
                    Text("Copy to Clipboard")
                        .fontWeight(.medium)
                }
                .font(.subheadline)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 12)
                .background(Color.white.opacity(0.2))
                .clipShape(RoundedRectangle(cornerRadius: 10))
            }
        }
        .padding(16)
        .background(Color.black.opacity(0.2))
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }
}

// Glass-style text field
struct GlassTextFieldStyle: TextFieldStyle {
    func _body(configuration: TextField<Self._Label>) -> some View {
        configuration
            .padding()
            .background(Color.white.opacity(0.2))
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .foregroundColor(.white)
            .font(.body)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.white.opacity(0.3), lineWidth: 1)
            )
    }
}

// Flow layout for wrapping topics
struct FlowLayout: Layout {
    var spacing: CGFloat = 8
    
    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let result = FlowResult(
            in: proposal.replacingUnspecifiedDimensions().width,
            subviews: subviews,
            spacing: spacing
        )
        return result.size
    }
    
    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let result = FlowResult(
            in: bounds.width,
            subviews: subviews,
            spacing: spacing
        )
        for (index, subview) in subviews.enumerated() {
            subview.place(at: CGPoint(x: bounds.minX + result.positions[index].x,
                                     y: bounds.minY + result.positions[index].y),
                         proposal: .unspecified)
        }
    }
    
    struct FlowResult {
        var size: CGSize = .zero
        var positions: [CGPoint] = []
        
        init(in maxWidth: CGFloat, subviews: Subviews, spacing: CGFloat) {
            var x: CGFloat = 0
            var y: CGFloat = 0
            var lineHeight: CGFloat = 0
            
            for subview in subviews {
                let size = subview.sizeThatFits(.unspecified)
                
                if x + size.width > maxWidth && x > 0 {
                    x = 0
                    y += lineHeight + spacing
                    lineHeight = 0
                }
                
                positions.append(CGPoint(x: x, y: y))
                lineHeight = max(lineHeight, size.height)
                x += size.width + spacing
            }
            
            self.size = CGSize(width: maxWidth, height: y + lineHeight)
        }
    }
}

// MARK: - Preview

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .environmentObject(AppSettings())
    }
}
