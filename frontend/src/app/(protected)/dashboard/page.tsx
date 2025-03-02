import ActivityFeed from '@/components/dashboard/activity-feed';
import { CommitFeed } from '@/components/dashboard/Commits/commit-feed';
import { MeetingCard } from '@/components/dashboard/meeting-card';
import { QuestionCard } from '@/components/dashboard/question-card';
import { TopBar } from '@/components/dashboard/top-bar';

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-[#FAFAFA] p-6">
      {/* <TopBar /> */}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <QuestionCard />
        <MeetingCard />
      </div>
      {/* Optimize This even Though Commits are same , it sends req to backend when Project is changed */}
      <CommitFeed />
    </div>
  );
}
