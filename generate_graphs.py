import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter
file_a='fleet-simulation-scenario-a-fiber-0.1pct-2026-03-27T15-28-45-426Z.csv'
file_b='fleet-simulation-scenario-b-4g-1.2pct-2026-03-27T15-37-05-383Z.csv'
file_c='fleet-simulation-scenario-c-rural-3.5pct-2026-03-27T15-45-03-272Z.csv'
df_a=pd.read_csv(file_a).query("status=='ok'").copy()
df_b=pd.read_csv(file_b).query("status=='ok'").copy()
df_c=pd.read_csv(file_c).query("status=='ok'").copy()
df_a['Scenario']='Scenario A: Fiber (0.1% Loss)'
df_b['Scenario']='Scenario B: 4G Mobile (1.2% Loss)'
df_c['Scenario']='Scenario C: Rural Edge (3.5% Loss)'
df_all=pd.concat([df_a,df_b,df_c])
palette={'Scenario A: Fiber (0.1% Loss)':'#2b7bba','Scenario B: 4G Mobile (1.2% Loss)':'#e77b4d','Scenario C: Rural Edge (3.5% Loss)':'#c12640'}
print(f"Dataset successfully loaded. Total successful data points:{len(df_all)}")
plt.figure(figsize=(10,6))
means=df_all.groupby('Scenario')[['baseline_ttfb_ms','pqc_ttfb_ms']].mean().reset_index()
means_melted=means.melt(id_vars='Scenario',var_name='Metric',value_name='Time (ms)')
means_melted['Metric']=means_melted['Metric'].map({'baseline_ttfb_ms':'Classical Baseline TTFB','pqc_ttfb_ms':'Simulated PQC Hybrid TTFB'})
ax1=sns.barplot(data=means_melted,x='Scenario',y='Time (ms)',hue='Metric',palette='mako')
plt.title('Empirical Average TLS Handshake Latency: Classical vs. PQC',fontsize=14,fontweight='bold',pad=15)
plt.ylabel('Time-To-First-Byte (ms)',fontsize=12,fontweight='bold')
plt.xlabel('Network Profile',fontsize=12,fontweight='bold')
plt.xticks(fontsize=11)
plt.legend(title='Handshake Protocol',fontsize=11,title_fontsize=12)
for p in ax1.patches:
    height=p.get_height()
    if not np.isnan(height)and height>0:
        ax1.annotate(f"{height:.0f} ms",(p.get_x()+p.get_width()/2.,height),ha='center',va='bottom',xytext=(0,5),textcoords='offset points',fontsize=10,fontweight='bold')
plt.tight_layout()
plt.savefig('pqc_latency_comparison_bar.png',dpi=300,bbox_inches='tight')
plt.close()
plt.figure(figsize=(10,6))
ax2=sns.boxplot(data=df_all,x='Scenario',y='degradation_pct',palette='rocket',showfliers=False)
plt.title('Distribution of PQC Latency Degradation Penalty',fontsize=14,fontweight='bold',pad=15)
plt.ylabel('Latency Degradation (%)',fontsize=12,fontweight='bold')
plt.xlabel('Network Profile',fontsize=12,fontweight='bold')
plt.xticks(fontsize=11)
medians=df_all.groupby(['Scenario'])['degradation_pct'].median().values
pos=range(len(medians))
for tick,label in zip(pos,ax2.get_xticklabels()):
    ax2.text(pos[tick],medians[tick]+5,f"Median:\n{medians[tick]:.1f}%",horizontalalignment='center',size='medium',color='white',weight='semibold',bbox=dict(facecolor='black',alpha=0.5,edgecolor='none',boxstyle='round,pad=0.2'))
plt.tight_layout()
plt.savefig('pqc_degradation_boxplot.png',dpi=300,bbox_inches='tight')
plt.close()
plt.figure(figsize=(10,6))
sns.scatterplot(data=df_all,x='baseline_rtt_ms',y='pqc_ttfb_ms',hue='Scenario',palette=palette,alpha=0.7,edgecolor='k',s=60)
max_val=max(df_all['baseline_rtt_ms'].max(),df_all['pqc_ttfb_ms'].max())
plt.plot([0,max_val],[0,max_val],'k--',alpha=0.3,label='1:1 Ratio (Theoretical Ideal)')
plt.title('Baseline RTT vs. Simulated PQC Handshake Latency',fontsize=14,fontweight='bold',pad=15)
plt.ylabel('Simulated PQC Handshake Latency (ms)',fontsize=12,fontweight='bold')
plt.xlabel('Classical Baseline RTT (ms)',fontsize=12,fontweight='bold')
plt.grid(True,linestyle='--',alpha=0.6)
plt.legend(title='Network Profile',fontsize=10,title_fontsize=11)
plt.tight_layout()
plt.savefig('pqc_rtt_scatter.png',dpi=300,bbox_inches='tight')
plt.close()
plt.figure(figsize=(10,6))
sns.ecdfplot(data=df_all,x='pqc_ttfb_ms',hue='Scenario',palette=palette,linewidth=2.5)
plt.axvline(x=300,color='gray',linestyle='--',alpha=0.8,linewidth=1.5,label='300ms (Warning Threshold)')
plt.axvline(x=500,color='red',linestyle='--',alpha=0.8,linewidth=1.5,label='500ms (Critical Timeout)')
plt.title('Cumulative Distribution Function (CDF) of PQC Latency',fontsize=14,fontweight='bold',pad=15)
plt.ylabel('Cumulative Probability (%)',fontsize=12,fontweight='bold')
plt.xlabel('Simulated PQC Handshake Latency (ms)',fontsize=12,fontweight='bold')
plt.grid(True,linestyle='--',alpha=0.6)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.legend(loc='lower right',title='Network Profile & Thresholds',fontsize=10)
plt.tight_layout()
plt.savefig('pqc_latency_cdf.png',dpi=300,bbox_inches='tight')
plt.close()
print("\nSuccess! All 4 high-resolution graphs have been generated and saved.")
