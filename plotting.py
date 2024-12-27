import plotly.graph_objects as go
from plotly.subplots import make_subplots


#plotting code of the kinetics figure
def plot_kinetics(n,x,y):
    fig = go.Figure()

    for i in range(n):
        fig.add_trace(go.Scatter(x=x,y=y[i],name=r"$\mu_{k}(s)$".format(k=i+1)))

    fig.update_layout(xaxis_title='s',yaxis_title='', 
                    width=600, height=300,
                    margin=dict(l=0,r=0,b=0,t=10))

    # fig.show()
    return fig


def plot_u_critical(mu_hat, mu_max, e_list,u_c_list):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=e_list,y=u_c_list, name=r"$u_c(\varepsilon)$"))
    fig.add_trace(go.Scatter(x=[e_list[-1]],y=[mu_hat], name=r"$\hat{\mu}$", mode="markers"))
    fig.add_trace(go.Scatter(x=[e_list[0]],y=[mu_max], name=r"$\mu_{\max}$", mode="markers"))
    fig.update_layout(title="",xaxis_title=r"$\varepsilon$",yaxis_title=r"$u$", 
                    width=600, height=300,margin=dict(l=0,r=0,b=0,t=10))
    return fig


#plotting code of a single simulation (for all species, given an initial condition)
def plot_single_sim(n,t,X,S,x_star,s_star):
    fig = go.Figure()
    for i in range(n):
        fig.add_trace(go.Scatter(x=t,y=X[i],name=f"$x_{i+1}(t)$"))
    fig.add_trace(go.Scatter(x=t,y=S,name=r"$s(t)$"))
    fig.add_trace(go.Scatter(x=[t[-1] for i in range(n)],y=x_star,
                            name=r"$x^{\varepsilon,u}$", 
                            mode="markers",marker_line_width=2,
                            marker_color="red",marker_symbol="diamond",
                            marker_line_color="darkred",marker_size=5))
    fig.add_trace(go.Scatter(x=[t[-1]],y=[s_star],
                            name=r"$s^{\varepsilon,u}$", 
                            mode="markers", line_color="black",
                            marker_symbol="square",marker_line_width=2,
                            marker_color="red",marker_line_color="darkred",marker_size=5))
    fig.update_layout(xaxis_title='t',yaxis_title='', 
                    width=600, height=300,
                    margin=dict(l=0,r=0,b=0,t=10))

    return fig


#plotting code of the total biomass (B_m = s+sum x_i) 
def plot_total_mass(t,B_m):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t,y=B_m))
    fig.update_layout(title="Total Biomass",
                    xaxis_title='t',
                    yaxis_title='', 
                    width=600, height=300,
                    margin=dict(l=0,r=0,b=0,t=50))
    return fig


#plotting code of the distance to E0 figure
def plot_distance(e_list,u_list,distances,u_c_list, mu_hat, mu_max):
    fig = make_subplots(specs=[[{"secondary_y": True,"r":0.05}]],shared_xaxes=True)

    fig.add_trace(go.Heatmap(
            z=distances,
            x=e_list,
            y=u_list,
            colorscale='Viridis',
            colorbar={"titleside":'bottom',  
                    "titlefont":dict(size=14, family='Times New Roman'),  
                    "len":0.8, 
                    "x":0.85,"y":0.6}))
        

    fig.add_trace(go.Scatter(
        mode='lines', 
        x=e_list, 
        y=u_c_list,
        line=dict(color='red',width=2),
        legend="legend2",
        showlegend=True, name=r"$u_c(\varepsilon)$"), secondary_y=False,)
                
    fig.add_trace(go.Scatter(x=[e_list[-1]],y=[mu_hat], name=r"$\hat{\mu}$",
                              mode="markers",
                              marker=dict(size=10),
                              legend="legend2",
                              showlegend=True), secondary_y=False)
    fig.add_trace(go.Scatter(x=[e_list[0]],y=[mu_max], name=r"$\mu_{\max}$", 
                             mode="markers",
                             marker=dict(size=10),
                             legend="legend2",
                             showlegend=True), secondary_y=False)

    fig.update_layout(xaxis_title=r'$\varepsilon$',
                    yaxis_title=r'$u$', 
                    width=600, height=300,
                    margin=dict(l=0,r=0,b=0,t=0), 
                    legend2={
                        "y": -0.1,
                        "x": 0.95
                        },
                    plot_bgcolor='rgba(0,0,0,0)'
                    )

    return fig


#plotting code of the verification if J is hurwitz
def plot_hurwitz_test(e_list,u_list,lambda_J_matrix,u_c_list):
    fig = make_subplots(specs=[[{"secondary_y": True,"r":0.05}]],shared_xaxes=True)

    fig.add_trace(go.Heatmap(
            z=lambda_J_matrix,
            x=e_list,
            y=u_list, colorscale='Plasma',
            colorbar={"titleside":'bottom',  
                    "titlefont":dict(size=14, family='Times New Roman'),
                    "x":0.76,"y":0.53}))

    fig.add_trace(go.Scatter(
        mode='lines', 
        x=e_list, 
        y=u_c_list,
        line=dict(color='red',width=2),
        legend="legend2",
        showlegend=True, name=r"$u_c(\varepsilon)$"), secondary_y=False,)
                
    fig.update_layout(xaxis_title=r'$\varepsilon$',
                    yaxis_title=r'$u$', 
                    width=600, height=300,
                    margin=dict(l=0,r=0,b=0,t=0), 
                    legend2={
                        "y": -0.1,
                        "x": 0.86
                        }
                    )
    return fig


# plotting code for simulation on trajectories on a set of initial conditions
def plot_multiple_sim(n, N_IC, T_f, y_star, t, graph):
    row_column = {0:(1,2),1:(1,3),2:(2,1),3:(2,2),4:(2,3),5:(1,1)}
    fig = make_subplots(rows=2, cols=3)

    for i in range(n+1):
        graph_i = graph[i]
        r,c = row_column[i]
        for j in range(N_IC):
            y = graph_i[j]
            fig.add_trace(go.Scatter(x=t,y=y,showlegend=False,mode="lines", line_width=0.5), row=r,col=c)

        text=r"$\hspace{{-0.2cm}}x^{{\varepsilon,u}}_{i}$".format(i=i+1) if(i<n) else r"$s^{{\varepsilon,u}}$"
        fig.add_trace(go.Scatter(x=[T_f],y=[y_star[i]], text=text,mode="markers+text",marker_line_width=0, textposition="top left",
                            marker_color="black",marker_size=6,showlegend=False), row=r,col=c)
        fig.update_xaxes(title_text=r"$t$", row=r, col=c, range=[-1, T_f+5],title_standoff = 5)
        title_y = r"$x_{i}$".format(i=i+1) if(i<n) else r"$s$"
        s_off = 0 if(i<n) else 5
        fig.update_yaxes(title_text=title_y, row=r, col=c, title_standoff = s_off)

    fig.update_layout(width=900, height=450,margin=dict(l=20,r=20,b=20,t=20))

    return fig


# plotting code for simulation on trajectories on two different sets of initial conditions
def plot_multiple_sim_delta(n, N_IC, T_f, y_star, t, graph1, graph2):
    row_column = {0:(1,2),1:(1,3),2:(2,1),3:(2,2),4:(2,3),5:(1,1)}
    fig = make_subplots(rows=2, cols=3)

    for i in range(n+1):
        r,c = row_column[i]

        graph_i = graph1[i]
        color = "magenta"
        for j in range(N_IC):
            y = graph_i[j]
            fig.add_trace(go.Scatter(x=t,y=y,showlegend=False,mode="lines", line_color=color, line_width=0.5), row=r,col=c)
        
        graph_i = graph2[i]
        color = "orange"
        for j in range(N_IC):
            y = graph_i[j]
            fig.add_trace(go.Scatter(x=t,y=y,showlegend=False,mode="lines", line_color=color, line_width=0.5), row=r,col=c)
        
        txp = "top left" if(i != 0) else "bottom left"
        text=r"$x^{{\varepsilon,u}}_{i}$".format(i=i+1) if(i<n) else r"$s^{{\varepsilon,u}}$"
        fig.add_trace(go.Scatter(x=[T_f],y=[y_star[i]], text=text,mode="markers+text",marker_line_width=0, textposition=txp,
                            marker_color="black",marker_size=6,showlegend=False), row=r,col=c)
        
        
        fig.update_xaxes(title_text=r"$t$", row=r, col=c, range=[-1, T_f+5],title_standoff = 5)
        title_y = r"$x_{i}$".format(i=i+1) if(i<n) else r"$s$"
        s_off = 0 if(i<n) else 5
        fig.update_yaxes(title_text=title_y, row=r, col=c, title_standoff = s_off)
    fig.update_layout(width=800, height=450,margin=dict(l=20,r=20,b=20,t=20))
    return fig