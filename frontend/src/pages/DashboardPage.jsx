import React from 'react'
import DashboardCard from '../components/DashboardCards.jsx';
import SlackChart from '../components/SlackChart.jsx';

const DashboardPage = () => {
  return (
    <div className="p-8 mt-6 ">
      <div className="flex flex-wrap gap-6 items-stretch">
        <div className="flex-shrink-0 h-[430px]">
          <DashboardCard
            title="Slack Count"
            value="120"
            icon={<div className="w-6 h-6 bg-green-500 rounded-full"></div>}
            className="!h-full"
          />
        </div>
        <div className="flex-1 min-w-[300px] max-w-3xl">
          <SlackChart/>
        </div>
      </div>
    </div>
    
  )
}

export default DashboardPage;
